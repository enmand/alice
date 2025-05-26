from datetime import datetime
from typing import Tuple, override
from uuid import UUID, uuid4

from google.protobuf.empty_pb2 import Empty
from google.protobuf.json_format import MessageToDict, ParseDict
from google.protobuf.timestamp_pb2 import Timestamp
from grpc import ServicerContext
from jambo.schema_converter import JSONSchema
from pydantic.json_schema import JsonSchemaValue

from graph.v1.graph_pb2 import Edge, Episode, Node
from ingest.ingest import Ingester, Record, Records
from ingest.v1.ingest_pb2 import (AddEntityRequest, AddEntityResponse,
                                  DeleteEntityRequest)
from ingest.v1.ingest_pb2 import Entity as ProtoEntity
from ingest.v1.ingest_pb2 import (GetEntityRequest, GetEntityResponse,
                                  IngestRequest, IngestResponse,
                                  UpdateEntityRequest)
from ingest.v1.ingest_pb2_grpc import IngestServiceServicer
from ingest.v1.jsonschema_pb2 import JSONSchema as ProtoJSONSchema
from models import (RECORDS_ROLE_MAPPING, RECORDS_SOURCE_TYPE_MAPPING, Entity,
                    Identity)


class IngestServicer(IngestServiceServicer):
    ingester: Ingester

    def __init__(self, ingester: Ingester):
        self.ingester = ingester

    @override
    async def Ingest(
        self,
        request: IngestRequest,
        context: ServicerContext | None,
    ) -> IngestResponse:
        records = await self.ingester.ingest(
            Records(
                group_id=request.group_id,
                records=[
                    Record(
                        valid_at=m.timestamp.ToDatetime(),
                        uuid=UUID(m.uuid) if m.uuid else None,
                        previous=[UUID(prev) for prev in m.previous],
                        timestamp=m.timestamp.ToDatetime(),
                        name=m.name,
                        data=m.data,
                        identity=Identity(
                            name=m.identity.name,
                            role=RECORDS_ROLE_MAPPING[m.identity.role],
                        ),
                        community_update=m.community_update,
                        source_description=m.source_description,
                        source_type=RECORDS_SOURCE_TYPE_MAPPING[m.source_type],
                        entities=list(m.entities) if m.entities else [],
                    )
                    for m in request.records
                ],
            )
        )

        return IngestResponse(
            group_id=request.group_id,
            episodes=[
                Episode(
                    uuid=m.uuid.__str__() if m.uuid else None,
                    valid_at=Timestamp().FromDatetime(m.valid_at),
                    nodes=[
                        Node(
                            uuid=n.uuid.__str__() if n.uuid else None,
                            summary=n.summary,
                        )
                        for _, n in enumerate(m.nodes if m.nodes else [])
                    ],
                    edges=[
                        Edge(
                            fact=e.fact,
                            name=e.name,
                            valid_at=(
                                Timestamp().FromDatetime(e.valid_at)
                                if e.valid_at
                                else None
                            ),
                        )
                        for _, e in enumerate(m.edges if m.edges else [])
                    ],
                )
                for _, m in enumerate(records)
            ],
        )

    @override
    async def AddEntity(
        self,
        request: AddEntityRequest,
        context: ServicerContext | None = None,
    ) -> AddEntityResponse:
        (schema, valid_at) = validate_entity_request(request)

        # Add the entity using the ingester
        id = await self.ingester.add_entity(
            request.group_id,
            Entity(
                id=UUID(request.entity.id, version=4) if request.entity.id else uuid4(),
                schema=JsonSchemaValue(schema),
                name=request.entity.name,
                tags=list(request.entity.tags) or [],
                description=request.entity.description,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                valid_at=valid_at,
            ),
        )

        return AddEntityResponse(id=id.__str__())

    @override
    async def GetEntity(
        self, request: GetEntityRequest, context: ServicerContext | None = None
    ) -> GetEntityResponse:
        if request.id != "":
            entity_id = UUID(request.id, version=4)
            entity = await self.ingester.get_entity(
                request.group_id, entity_id=entity_id
            )
        elif request.schema_id != "":
            entity = await self.ingester.get_entity(
                request.group_id, schema_id=request.schema_id
            )
        else:
            raise ValueError("Either id or schema_id must be provided in the request")

        pr = ProtoEntity(
            id=entity.id.__str__(),
            name=entity.name,
            description=entity.description,
            schema=ParseDict(denormalize_json_schema(entity.schema), ProtoJSONSchema()),
        )
        if entity.valid_at:
            pr.valid_at.FromDatetime(entity.valid_at)

        return GetEntityResponse(entity=pr)

    @override
    async def UpdateEntity(
        self, request: UpdateEntityRequest, context: ServicerContext | None = None
    ) -> Empty:
        (schema, valid_at) = validate_entity_request(request)
        if not request.entity or not request.entity.id:
            raise ValueError("Entity and entity ID must be provided in the request")

        entity_id = UUID(request.entity.id, version=4)
        await self.ingester.update_entity(
            request.group_id,
            entity_id,
            Entity(
                id=entity_id,
                schema=JsonSchemaValue(schema),
                name=request.entity.name,
                tags=list(request.entity.tags) or [],
                description=request.entity.description,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                valid_at=valid_at,
            ),
        )

        return Empty()

    @override
    async def DeleteEntity(
        self, request: DeleteEntityRequest, context: ServicerContext | None = None
    ) -> Empty:
        if request.id != "":
            entity_id = UUID(request.id, version=4)
            await self.ingester.delete_entity(request.group_id, entity_id=entity_id)
        elif request.schema_id != "":
            await self.ingester.delete_entity(
                request.group_id, schema_id=request.schema_id
            )
        else:
            raise ValueError("Either id or schema_id must be provided in the request")

        return Empty()


def validate_entity_request(
    request: AddEntityRequest | UpdateEntityRequest,
) -> Tuple[JSONSchema, datetime]:
    if not request.entity:
        raise ValueError("Entity must be provided in the request")

    if not request.entity.schema:
        raise ValueError("Schema must be provided in the request")
    if not request.entity.name:
        raise ValueError("Entity name must be provided in the request")

    schema = normalize_jsonschema_types(
        MessageToDict(request.entity.schema, preserving_proto_field_name=True)
    )

    if not schema.get("type"):
        raise ValueError("Schema type must be provided in the request")

    valid_at = (
        request.entity.valid_at.ToDatetime()
        if request.entity.valid_at
        else datetime.now()
    )
    return JSONSchema(**schema), valid_at


def normalize_jsonschema_types(schema: dict) -> dict:
    """
    Recursively normalize the 'type' field in a JSONSchema dictionary.
    If 'type' is a list with a single element, convert it to a string.
    """
    if (
        "type" in schema
        and isinstance(schema["type"], list)
        and len(schema["type"]) == 1
    ):
        schema["type"] = schema["type"][0]  # Convert single-element list to string

    if "schema" in schema:
        schema["$schema"] = schema["schema"]
        del schema["schema"]
    if "id" in schema:
        schema["$id"] = schema["id"]
        del schema["id"]
    # Recursively process nested JSONSchema objects
    for key in ["properties", "patternProperties"]:
        if key in schema and isinstance(schema[key], dict):
            schema[key] = {
                k: normalize_jsonschema_types(v) for k, v in schema[key].items()
            }

    # Handle additionalProperties, items, and other JSONSchema fields
    if "additionalProperties" in schema and isinstance(
        schema["additionalProperties"], dict
    ):
        schema["additionalProperties"] = normalize_jsonschema_types(
            schema["additionalProperties"]
        )

    if "items" in schema:
        if isinstance(schema["items"], dict):
            schema["items"] = normalize_jsonschema_types(schema["items"])
        elif isinstance(schema["items"], list):
            schema["items"] = [
                normalize_jsonschema_types(item) for item in schema["items"]
            ]

    # Recursively process combination keywords (allOf, anyOf, oneOf, not)
    for key in ["allOf", "anyOf", "oneOf"]:
        if key in schema and isinstance(schema[key], list):
            schema[key] = [
                normalize_jsonschema_types(subschema) for subschema in schema[key]
            ]

    for key in ["not", "if", "then", "else"]:
        if key in schema and isinstance(schema[key], dict):
            schema[key] = normalize_jsonschema_types(schema[key])

    return schema


def denormalize_json_schema(schema: JsonSchemaValue | None) -> dict:
    """
    Convert a normalized JSON Schema dictionary to a ProtoJSONSchema object.
    """
    type_ = schema.get("type", [])
    if isinstance(type_, str):
        type_ = [type_]

    proto_schema = {
        "id": schema.get("$id", ""),
        "schema": schema.get("$schema", ""),
        "type": type_,
    }

    for key, value in schema.items():
        if key in {"$id", "$schema", "type"}:
            continue

        if isinstance(value, dict):
            proto_schema[key] = denormalize_json_schema(value)
        elif isinstance(value, list):
            proto_schema[key] = [
                denormalize_json_schema(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            proto_schema[key] = value

    return proto_schema
