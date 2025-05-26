from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JSONSchema(_message.Message):
    __slots__ = ("schema", "id", "title", "description", "default", "examples", "type", "properties", "required", "additional_properties", "min_properties", "max_properties", "pattern_properties", "dependencies", "items", "additional_items", "min_items", "max_items", "unique_items", "min_length", "max_length", "pattern", "format", "minimum", "maximum", "exclusive_minimum", "exclusive_maximum", "multiple_of", "enum", "const", "then", "all_of", "any_of", "one_of")
    class PropertiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: JSONSchema
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[JSONSchema, _Mapping]] = ...) -> None: ...
    class PatternPropertiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: JSONSchema
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[JSONSchema, _Mapping]] = ...) -> None: ...
    class DependenciesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    EXAMPLES_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    MIN_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    MAX_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    PATTERN_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    DEPENDENCIES_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_ITEMS_FIELD_NUMBER: _ClassVar[int]
    MIN_ITEMS_FIELD_NUMBER: _ClassVar[int]
    MAX_ITEMS_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_ITEMS_FIELD_NUMBER: _ClassVar[int]
    MIN_LENGTH_FIELD_NUMBER: _ClassVar[int]
    MAX_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_FIELD_NUMBER: _ClassVar[int]
    MAXIMUM_FIELD_NUMBER: _ClassVar[int]
    EXCLUSIVE_MINIMUM_FIELD_NUMBER: _ClassVar[int]
    EXCLUSIVE_MAXIMUM_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_OF_FIELD_NUMBER: _ClassVar[int]
    ENUM_FIELD_NUMBER: _ClassVar[int]
    CONST_FIELD_NUMBER: _ClassVar[int]
    IF_FIELD_NUMBER: _ClassVar[int]
    THEN_FIELD_NUMBER: _ClassVar[int]
    ELSE_FIELD_NUMBER: _ClassVar[int]
    ALL_OF_FIELD_NUMBER: _ClassVar[int]
    ANY_OF_FIELD_NUMBER: _ClassVar[int]
    ONE_OF_FIELD_NUMBER: _ClassVar[int]
    NOT_FIELD_NUMBER: _ClassVar[int]
    schema: str
    id: str
    title: str
    description: str
    default: _struct_pb2.Value
    examples: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Value]
    type: _containers.RepeatedScalarFieldContainer[str]
    properties: _containers.MessageMap[str, JSONSchema]
    required: _containers.RepeatedScalarFieldContainer[str]
    additional_properties: _struct_pb2.Value
    min_properties: int
    max_properties: int
    pattern_properties: _containers.MessageMap[str, JSONSchema]
    dependencies: _containers.MessageMap[str, _struct_pb2.Value]
    items: _struct_pb2.Value
    additional_items: _struct_pb2.Value
    min_items: int
    max_items: int
    unique_items: bool
    min_length: int
    max_length: int
    pattern: str
    format: str
    minimum: float
    maximum: float
    exclusive_minimum: float
    exclusive_maximum: float
    multiple_of: float
    enum: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Value]
    const: _struct_pb2.Value
    then: JSONSchema
    all_of: _containers.RepeatedCompositeFieldContainer[JSONSchema]
    any_of: _containers.RepeatedCompositeFieldContainer[JSONSchema]
    one_of: _containers.RepeatedCompositeFieldContainer[JSONSchema]
    def __init__(self, schema: _Optional[str] = ..., id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., default: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., examples: _Optional[_Iterable[_Union[_struct_pb2.Value, _Mapping]]] = ..., type: _Optional[_Iterable[str]] = ..., properties: _Optional[_Mapping[str, JSONSchema]] = ..., required: _Optional[_Iterable[str]] = ..., additional_properties: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., min_properties: _Optional[int] = ..., max_properties: _Optional[int] = ..., pattern_properties: _Optional[_Mapping[str, JSONSchema]] = ..., dependencies: _Optional[_Mapping[str, _struct_pb2.Value]] = ..., items: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., additional_items: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., min_items: _Optional[int] = ..., max_items: _Optional[int] = ..., unique_items: bool = ..., min_length: _Optional[int] = ..., max_length: _Optional[int] = ..., pattern: _Optional[str] = ..., format: _Optional[str] = ..., minimum: _Optional[float] = ..., maximum: _Optional[float] = ..., exclusive_minimum: _Optional[float] = ..., exclusive_maximum: _Optional[float] = ..., multiple_of: _Optional[float] = ..., enum: _Optional[_Iterable[_Union[_struct_pb2.Value, _Mapping]]] = ..., const: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., then: _Optional[_Union[JSONSchema, _Mapping]] = ..., all_of: _Optional[_Iterable[_Union[JSONSchema, _Mapping]]] = ..., any_of: _Optional[_Iterable[_Union[JSONSchema, _Mapping]]] = ..., one_of: _Optional[_Iterable[_Union[JSONSchema, _Mapping]]] = ..., **kwargs) -> None: ...
