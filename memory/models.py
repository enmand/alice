from datetime import datetime
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.json_schema import GenerateJsonSchema, JsonSchemaValue
from referencing.jsonschema import DRAFT202012

from ingest.v1.ingest_pb2 import RecordsRole, RecordsSourceType

RECORDS_ROLE_MAPPING: dict[RecordsRole, Literal["user", "assistant", "system"]] = {
    RecordsRole.RECORDS_ROLE_UNSPECIFIED: "user",
    RecordsRole.RECORDS_ROLE_USER: "user",
    RecordsRole.RECORDS_ROLE_ASSISTANT: "assistant",
    RecordsRole.RECORDS_ROLE_SYSTEM: "system",
}

RECORDS_SOURCE_TYPE_MAPPING: dict[
    RecordsSourceType, Literal["message", "json", "text"]
] = {
    RecordsSourceType.RECORDS_SOURCE_TYPE_UNSPECIFIED: "text",
    RecordsSourceType.RECORDS_SOURCE_TYPE_MESSAGE: "message",
    RecordsSourceType.RECORDS_SOURCE_TYPE_JSON: "json",
    RecordsSourceType.RECORDS_SOURCE_TYPE_TEXT: "text",
}


class Identity(BaseModel):
    name: str = Field(description="Name of the identity")
    role: Literal["user", "assistant", "system"]


class Node(BaseModel):
    uuid: UUID = Field(description="UUID of the node")
    summary: str = Field(description="Summary of the node")


class Edge(BaseModel):
    fact: str = Field(description="Fact of the edge")
    name: str = Field(description="Name of the edge")
    valid_at: datetime | None = Field(
        description="Valid at timestamp of the edge",
        alias="valid_at",
    )


class Record(BaseModel):
    uuid: UUID | None = Field(description="UUID of the record")
    previous: List[UUID] = Field(
        description="UUID of the previous parent record",
        alias="previous",
    )
    timestamp: datetime = Field(
        description="Timestamp of the record",
        alias="timestamp",
    )
    name: str = Field(description="Name of the record")
    data: str = Field(description="Data of the record")
    identity: Identity = Field(
        description="Identity of the record",
        alias="identity",
    )
    community_update: bool = Field(
        description="Community update flag of the record",
        alias="community_update",
    )
    source_description: str = Field(
        description="Description of the source of the record"
    )
    source_type: Literal["text", "message", "json"] = Field(
        description="Type of the source of the record"
    )
    valid_at: datetime = Field(
        description="Valid at timestamp of the record",
        alias="valid_at",
    )
    nodes: List[Node] | None = Field(
        description="List of nodes associated with the record",
        alias="nodes",
        default=None,
    )
    edges: List[Edge] | None = Field(
        description="List of edges associated with the record",
        alias="edges",
        default=None,
    )
    entities: Optional[List[UUID] | List[str]] = Field(
        description="List of entities associated with the record",
        alias="entities",
        default=None,
    )


class Records(BaseModel):
    records: List[Record] = Field(
        description="List of records",
        alias="records",
    )
    group_id: str = Field(
        description="Group ID of the record",
        alias="group_id",
    )


class Entity(BaseModel):
    id: UUID = Field(description="id of the entity")
    name: str | None = Field(description="Name of the entity", default=None)
    description: str | None = Field(
        description="Description of the entity", default=None
    )
    schema: JsonSchemaValue | None = Field(
        description="Schema of the entity", default=None
    )
    tags: List[str] | None = Field(
        description="Tags associated with the entity",
        alias="tags",
        default=None,
    )
    created_at: datetime | None = Field(
        description="Created at timestamp of the entity",
        alias="created_at",
        default=None,
    )
    updated_at: datetime | None = Field(
        description="Updated at timestamp of the entity",
        alias="updated_at",
        default=None,
    )
    valid_at: datetime | None = Field(
        description="Valid at timestamp of the entity",
        alias="valid_at",
        default=None,
    )
