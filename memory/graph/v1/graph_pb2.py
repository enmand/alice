# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: graph/v1/graph.proto
# Protobuf Python Version: 5.29.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    3,
    '',
    'graph/v1/graph.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14graph/v1/graph.proto\x12\x08graph.v1\x1a\x1fgoogle/protobuf/timestamp.proto\"\xa0\x01\n\x07\x45pisode\x12\x12\n\x04uuid\x18\x01 \x01(\tR\x04uuid\x12\x35\n\x08valid_at\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x07validAt\x12$\n\x05nodes\x18\x03 \x03(\x0b\x32\x0e.graph.v1.NodeR\x05nodes\x12$\n\x05\x65\x64ges\x18\x04 \x03(\x0b\x32\x0e.graph.v1.EdgeR\x05\x65\x64ges\"4\n\x04Node\x12\x12\n\x04uuid\x18\x01 \x01(\tR\x04uuid\x12\x18\n\x07summary\x18\x02 \x01(\tR\x07summary\"\x8b\x02\n\x04\x45\x64ge\x12\x12\n\x04uuid\x18\x01 \x01(\tR\x04uuid\x12\x12\n\x04\x66\x61\x63t\x18\x02 \x01(\tR\x04\x66\x61\x63t\x12\x12\n\x04name\x18\x03 \x01(\tR\x04name\x12\x1a\n\x08\x65pisodes\x18\x04 \x03(\tR\x08\x65pisodes\x12\x39\n\nexpired_at\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\texpiredAt\x12\x39\n\ninvalid_at\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tinvalidAt\x12\x35\n\x08valid_at\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x07validAtB4Z2github.com/enmand/alice/generated/graph/v1;graphv1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'graph.v1.graph_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z2github.com/enmand/alice/generated/graph/v1;graphv1'
  _globals['_EPISODE']._serialized_start=68
  _globals['_EPISODE']._serialized_end=228
  _globals['_NODE']._serialized_start=230
  _globals['_NODE']._serialized_end=282
  _globals['_EDGE']._serialized_start=285
  _globals['_EDGE']._serialized_end=552
# @@protoc_insertion_point(module_scope)
