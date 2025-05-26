import logging
from typing import Dict, List, Optional
from uuid import UUID

from graphiti_core.graphiti import AddEpisodeResults, Graphiti
from graphiti_core.nodes import EpisodeType
from jambo.schema_converter import JSONSchema, SchemaConverter
from pydantic import BaseModel
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

import db.models as db_models
from models import Edge, Entity, Node, Record, Records


class Ingester:
    __graphiti: Graphiti
    __db: Engine

    def __init__(self, graphiti: Graphiti, db: Engine):
        self.graphiti = graphiti
        self.db = db

    async def ingest(self, records: Records) -> list[Record]:
        ingested: list[Record] = []

        def _extract_entities_type[T](
            records: Records,
            _typ: type[T] = str,
        ) -> Optional[List[T]]:
            [
                e
                for r in records.records
                if r.entities is not None
                for e in r.entities
                if isinstance(e, _typ)
            ]

        record_entities_uuids = _extract_entities_type(records, UUID) or []
        record_entities_strs = _extract_entities_type(records, str) or []

        entities: Optional[Dict[str, BaseModel]] = None
        if record_entities_uuids or record_entities_strs:
            with Session(self.db) as session:
                found_entities = (
                    session.query(db_models.Entity)
                    .filter(
                        db_models.Entity.group_id == records.group_id,
                        db_models.Entity.id.in_(record_entities_uuids),
                        db_models.Entity.schema["$id"].astext.in_(record_entities_strs),
                    )
                    .all()
                )

                # Calculate missing IDs
                found_entity_ids = {e.id for e in found_entities}
                found_entity_schema_ids = {
                    e.schema["$id"].astext for e in found_entities
                }
                all_entity_ids = set(record_entities_uuids + record_entities_strs)
                missing_ids = (
                    all_entity_ids - found_entity_ids - found_entity_schema_ids
                )

                if missing_ids:
                    raise ValueError(
                        f"Entities with IDs {missing_ids} not found in group {records.group_id}"
                    )
                # Convert found entities to a dictionary for quick lookup
                entities = {
                    e.schema["name"]: SchemaConverter.build(JSONSchema(**e.schema))()
                    for e in found_entities
                }

        for record in records.records:
            contents = record.data
            if record.source_type == "message":
                contents = "{} ({}): {}".format(
                    record.identity.name, record.identity.role, record.data
                )

            logging.info(f"Adding episode {record} with contents: {contents}")

            match await self.graphiti.add_episode(
                name=record.name,
                episode_body=contents,
                reference_time=record.timestamp,
                source_description=record.source_description,
                group_id=records.group_id,
                source=EpisodeType.from_str(record.source_type),
                uuid=record.uuid.__str__() if record.uuid else None,
                update_communities=record.community_update,
                entity_types=entities,
                previous_episode_uuids=list(
                    map(lambda x: x.__str__(), record.previous)
                ),
            ):
                case AddEpisodeResults(episode=episode, nodes=nodes, edges=edges):
                    pass

            ingested.append(
                Record(
                    uuid=UUID(episode.uuid, version=4),
                    previous=[],
                    timestamp=record.timestamp,
                    name=episode.name,
                    data=record.data,
                    identity=record.identity,
                    community_update=record.community_update,
                    source_description=episode.source_description,
                    source_type=episode.source.name,
                    valid_at=episode.valid_at,
                    nodes=[
                        Node(uuid=UUID(n.uuid, version=4), summary=n.summary)
                        for n in nodes
                    ],
                    edges=[
                        Edge(fact=e.fact, name=e.name, valid_at=e.valid_at)
                        for e in edges
                    ],
                )
            )

        return ingested

    async def add_entity(self, group_id: str, entity: Entity) -> UUID:
        logging.info(f"Adding entity {entity} with schema: {entity.schema}")

        with Session(self.db) as session:
            existing_entity = (
                session.query(db_models.Entity)
                .filter(
                    db_models.Entity.schema["$id"].astext == entity.schema["$id"],
                )
                .first()
            )

            if existing_entity is not None:
                raise ValueError(
                    f"Entity with ID {entity.schema["$id"]} already exists"
                )

        try:
            if entity.schema is None:
                raise ValueError("Schema cannot be None")

            _ = SchemaConverter.build(JSONSchema(**entity.schema))
        except ValueError as e:
            logging.error(f"Invalid JSON Schema: {e}")
            raise ValueError(f"Invalid JSON Schema: {e}")

        with Session(self.db) as session:
            db_entity = db_models.Entity(
                id=entity.id,
                group_id=group_id,
                name=entity.name,
                description=entity.description,
                created_at=entity.created_at,
                tags=entity.tags,
                updated_at=entity.updated_at,
                schema=entity.schema,
            )

            session.add(db_entity)
            session.commit()

        return entity.id

    async def get_entity(
        self, group_id: str, entity_id: UUID | None = None, schema_id: str | None = None
    ) -> Entity:
        logging.info(f"Getting entity entity_id:{entity_id}, schema_id:{schema_id}")

        with Session(self.db) as session:
            if entity_id is None and schema_id is None:
                raise ValueError("Either entity_id or schema_id must be provided")

            if entity_id is not None:
                db_entity = (
                    session.query(db_models.Entity)
                    .filter_by(group_id=group_id, id=entity_id)
                    .first()
                )

                if db_entity is None:
                    raise ValueError(f"Entity with ID {entity_id} not found")
            elif schema_id is not None:
                db_entity = (
                    session.query(db_models.Entity)
                    .filter_by(group_id=group_id)
                    .filter(db_models.Entity.schema["$id"].astext == schema_id)
                    .first()
                )

                if db_entity is None:
                    raise ValueError(f"Entity with schema ID {schema_id} not found")

            return Entity(
                id=db_entity.id,
                name=db_entity.name,
                description=db_entity.description,
                schema=db_entity.schema,
                tags=db_entity.tags,
                created_at=db_entity.created_at,
                updated_at=db_entity.updated_at,
            )

    async def update_entity(
        self, group_id: str, entity_id: UUID, entity: Entity
    ) -> None:
        logging.info(f"Updating entity {entity_id} with data: {entity}")
        with Session(self.db) as session:
            db_entity = (
                session.query(db_models.Entity)
                .filter_by(id=entity_id, group_id=group_id)
                .first()
            )

            if db_entity is None:
                raise ValueError(f"Entity with ID {entity_id} not found")

            if entity.schema is not None:
                try:
                    _ = SchemaConverter.build(JSONSchema(**entity.schema))
                except ValueError as e:
                    logging.error(f"Invalid JSON Schema: {e}")
                    raise ValueError(f"Invalid JSON Schema: {e}")
            else:
                raise ValueError("Schema cannot be None")

            db_entity.name = entity.name
            db_entity.description = entity.description
            db_entity.schema = entity.schema
            db_entity.updated_at = entity.updated_at
            db_entity.tags = entity.tags
            flag_modified(db_entity, "tags")

            session.merge(db_entity)
            session.flush()
            session.commit()

    async def delete_entity(
        self, group_id: str, entity_id: UUID | None = None, schema_id: str | None = None
    ) -> None:
        logging.info(f"Deleting entity {entity_id}")

        with Session(self.db) as session:
            if entity_id is not None:
                db_entity = (
                    session.query(db_models.Entity)
                    .filter_by(id=entity_id, group_id=group_id)
                    .first()
                )
            elif schema_id is not None:
                db_entity = (
                    session.query(db_models.Entity)
                    .filter_by(group_id=group_id)
                    .filter(db_models.Entity.schema["$id"].astext == schema_id)
                    .first()
                )
            else:
                raise ValueError("Either entity_id or schema_id must be provided")

            if db_entity is None:
                raise ValueError(f"Entity with ID {entity_id} not found")

            session.delete(db_entity)
            session.commit()
