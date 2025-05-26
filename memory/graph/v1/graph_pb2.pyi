from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Episode(_message.Message):
    __slots__ = ("uuid", "valid_at", "nodes", "edges")
    UUID_FIELD_NUMBER: _ClassVar[int]
    VALID_AT_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    EDGES_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    valid_at: _timestamp_pb2.Timestamp
    nodes: _containers.RepeatedCompositeFieldContainer[Node]
    edges: _containers.RepeatedCompositeFieldContainer[Edge]
    def __init__(self, uuid: _Optional[str] = ..., valid_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., nodes: _Optional[_Iterable[_Union[Node, _Mapping]]] = ..., edges: _Optional[_Iterable[_Union[Edge, _Mapping]]] = ...) -> None: ...

class Node(_message.Message):
    __slots__ = ("uuid", "summary")
    UUID_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    summary: str
    def __init__(self, uuid: _Optional[str] = ..., summary: _Optional[str] = ...) -> None: ...

class Edge(_message.Message):
    __slots__ = ("uuid", "fact", "name", "episodes", "expired_at", "invalid_at", "valid_at")
    UUID_FIELD_NUMBER: _ClassVar[int]
    FACT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    EPISODES_FIELD_NUMBER: _ClassVar[int]
    EXPIRED_AT_FIELD_NUMBER: _ClassVar[int]
    INVALID_AT_FIELD_NUMBER: _ClassVar[int]
    VALID_AT_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    fact: str
    name: str
    episodes: _containers.RepeatedScalarFieldContainer[str]
    expired_at: _timestamp_pb2.Timestamp
    invalid_at: _timestamp_pb2.Timestamp
    valid_at: _timestamp_pb2.Timestamp
    def __init__(self, uuid: _Optional[str] = ..., fact: _Optional[str] = ..., name: _Optional[str] = ..., episodes: _Optional[_Iterable[str]] = ..., expired_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., invalid_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., valid_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
