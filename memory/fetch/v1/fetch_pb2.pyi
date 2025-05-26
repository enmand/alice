from google.protobuf import timestamp_pb2 as _timestamp_pb2
from graph.v1 import graph_pb2 as _graph_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SearchRequest(_message.Message):
    __slots__ = ("group_id", "query", "central_node", "limit", "filters")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    CENTRAL_NODE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    group_id: _containers.RepeatedScalarFieldContainer[str]
    query: str
    central_node: str
    limit: int
    filters: Filters
    def __init__(self, group_id: _Optional[_Iterable[str]] = ..., query: _Optional[str] = ..., central_node: _Optional[str] = ..., limit: _Optional[int] = ..., filters: _Optional[_Union[Filters, _Mapping]] = ...) -> None: ...

class Filters(_message.Message):
    __slots__ = ("node_labels", "valid_at", "invalid_at", "created_at", "expired_at")
    NODE_LABELS_FIELD_NUMBER: _ClassVar[int]
    VALID_AT_FIELD_NUMBER: _ClassVar[int]
    INVALID_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    EXPIRED_AT_FIELD_NUMBER: _ClassVar[int]
    node_labels: _containers.RepeatedScalarFieldContainer[str]
    valid_at: _containers.RepeatedCompositeFieldContainer[DateFilterGroups]
    invalid_at: _containers.RepeatedCompositeFieldContainer[DateFilterGroups]
    created_at: _containers.RepeatedCompositeFieldContainer[DateFilterGroups]
    expired_at: _containers.RepeatedCompositeFieldContainer[DateFilterGroups]
    def __init__(self, node_labels: _Optional[_Iterable[str]] = ..., valid_at: _Optional[_Iterable[_Union[DateFilterGroups, _Mapping]]] = ..., invalid_at: _Optional[_Iterable[_Union[DateFilterGroups, _Mapping]]] = ..., created_at: _Optional[_Iterable[_Union[DateFilterGroups, _Mapping]]] = ..., expired_at: _Optional[_Iterable[_Union[DateFilterGroups, _Mapping]]] = ...) -> None: ...

class DateFilterGroups(_message.Message):
    __slots__ = ("filters",)
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    filters: _containers.RepeatedCompositeFieldContainer[DateFilter]
    def __init__(self, filters: _Optional[_Iterable[_Union[DateFilter, _Mapping]]] = ...) -> None: ...

class DateFilter(_message.Message):
    __slots__ = ("date", "comparison_operator")
    DATE_FIELD_NUMBER: _ClassVar[int]
    COMPARISON_OPERATOR_FIELD_NUMBER: _ClassVar[int]
    date: _timestamp_pb2.Timestamp
    comparison_operator: str
    def __init__(self, date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., comparison_operator: _Optional[str] = ...) -> None: ...

class SearchResponse(_message.Message):
    __slots__ = ("group_id", "results")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    results: _containers.RepeatedCompositeFieldContainer[_graph_pb2.Edge]
    def __init__(self, group_id: _Optional[str] = ..., results: _Optional[_Iterable[_Union[_graph_pb2.Edge, _Mapping]]] = ...) -> None: ...
