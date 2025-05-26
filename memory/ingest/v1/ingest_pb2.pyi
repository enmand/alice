from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from graph.v1 import graph_pb2 as _graph_pb2
from ingest.v1 import jsonschema_pb2 as _jsonschema_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RecordsRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RECORDS_ROLE_UNSPECIFIED: _ClassVar[RecordsRole]
    RECORDS_ROLE_USER: _ClassVar[RecordsRole]
    RECORDS_ROLE_ASSISTANT: _ClassVar[RecordsRole]
    RECORDS_ROLE_SYSTEM: _ClassVar[RecordsRole]

class RecordsSourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RECORDS_SOURCE_TYPE_UNSPECIFIED: _ClassVar[RecordsSourceType]
    RECORDS_SOURCE_TYPE_MESSAGE: _ClassVar[RecordsSourceType]
    RECORDS_SOURCE_TYPE_JSON: _ClassVar[RecordsSourceType]
    RECORDS_SOURCE_TYPE_TEXT: _ClassVar[RecordsSourceType]
RECORDS_ROLE_UNSPECIFIED: RecordsRole
RECORDS_ROLE_USER: RecordsRole
RECORDS_ROLE_ASSISTANT: RecordsRole
RECORDS_ROLE_SYSTEM: RecordsRole
RECORDS_SOURCE_TYPE_UNSPECIFIED: RecordsSourceType
RECORDS_SOURCE_TYPE_MESSAGE: RecordsSourceType
RECORDS_SOURCE_TYPE_JSON: RecordsSourceType
RECORDS_SOURCE_TYPE_TEXT: RecordsSourceType

class IngestRequest(_message.Message):
    __slots__ = ("records", "group_id")
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    records: _containers.RepeatedCompositeFieldContainer[Record]
    group_id: str
    def __init__(self, records: _Optional[_Iterable[_Union[Record, _Mapping]]] = ..., group_id: _Optional[str] = ...) -> None: ...

class Record(_message.Message):
    __slots__ = ("uuid", "timestamp", "data", "source_description", "community_update", "previous", "name", "source_type", "identity", "entities")
    UUID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    SOURCE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    COMMUNITY_UPDATE_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    timestamp: _timestamp_pb2.Timestamp
    data: str
    source_description: str
    community_update: bool
    previous: _containers.RepeatedScalarFieldContainer[str]
    name: str
    source_type: RecordsSourceType
    identity: Identity
    entities: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, uuid: _Optional[str] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., data: _Optional[str] = ..., source_description: _Optional[str] = ..., community_update: bool = ..., previous: _Optional[_Iterable[str]] = ..., name: _Optional[str] = ..., source_type: _Optional[_Union[RecordsSourceType, str]] = ..., identity: _Optional[_Union[Identity, _Mapping]] = ..., entities: _Optional[_Iterable[str]] = ...) -> None: ...

class Identity(_message.Message):
    __slots__ = ("name", "role")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    name: str
    role: RecordsRole
    def __init__(self, name: _Optional[str] = ..., role: _Optional[_Union[RecordsRole, str]] = ...) -> None: ...

class IngestResponse(_message.Message):
    __slots__ = ("group_id", "episodes")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    EPISODES_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    episodes: _containers.RepeatedCompositeFieldContainer[_graph_pb2.Episode]
    def __init__(self, group_id: _Optional[str] = ..., episodes: _Optional[_Iterable[_Union[_graph_pb2.Episode, _Mapping]]] = ...) -> None: ...

class Entity(_message.Message):
    __slots__ = ("id", "name", "description", "tags", "valid_at", "schema")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    VALID_AT_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    valid_at: _timestamp_pb2.Timestamp
    schema: _jsonschema_pb2.JSONSchema
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., valid_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., schema: _Optional[_Union[_jsonschema_pb2.JSONSchema, _Mapping]] = ...) -> None: ...

class AddEntityRequest(_message.Message):
    __slots__ = ("group_id", "entity")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    entity: Entity
    def __init__(self, group_id: _Optional[str] = ..., entity: _Optional[_Union[Entity, _Mapping]] = ...) -> None: ...

class AddEntityResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetEntityRequest(_message.Message):
    __slots__ = ("group_id", "id", "schema_id")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    id: str
    schema_id: str
    def __init__(self, group_id: _Optional[str] = ..., id: _Optional[str] = ..., schema_id: _Optional[str] = ...) -> None: ...

class GetEntityResponse(_message.Message):
    __slots__ = ("entity",)
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    entity: Entity
    def __init__(self, entity: _Optional[_Union[Entity, _Mapping]] = ...) -> None: ...

class UpdateEntityRequest(_message.Message):
    __slots__ = ("group_id", "entity")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    entity: Entity
    def __init__(self, group_id: _Optional[str] = ..., entity: _Optional[_Union[Entity, _Mapping]] = ...) -> None: ...

class DeleteEntityRequest(_message.Message):
    __slots__ = ("group_id", "id", "schema_id")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    id: str
    schema_id: str
    def __init__(self, group_id: _Optional[str] = ..., id: _Optional[str] = ..., schema_id: _Optional[str] = ...) -> None: ...
