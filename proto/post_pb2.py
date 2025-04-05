# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/post.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10proto/post.proto\x12\x04post\"m\n\x11\x43reatePostRequest\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x12\n\ncreator_id\x18\x03 \x01(\t\x12\x12\n\nis_private\x18\x04 \x01(\x08\x12\x0c\n\x04tags\x18\x05 \x03(\t\"9\n\x12\x43reatePostResponse\x12\x0f\n\x07post_id\x18\x01 \x01(\t\x12\x12\n\ncreated_at\x18\x02 \x01(\t\"5\n\x11\x44\x65letePostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\"%\n\x12\x44\x65letePostResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"{\n\x11UpdatePostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\r\n\x05title\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12\x12\n\nis_private\x18\x05 \x01(\x08\x12\x0c\n\x04tags\x18\x06 \x03(\t\"(\n\x12UpdatePostResponse\x12\x12\n\nupdated_at\x18\x01 \x01(\t\"2\n\x0eGetPostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\"+\n\x0fGetPostResponse\x12\x18\n\x04post\x18\x01 \x01(\x0b\x32\n.post.Post\"C\n\x10ListPostsRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x0c\n\x04page\x18\x02 \x01(\x05\x12\x10\n\x08per_page\x18\x03 \x01(\x05\"\x8c\x01\n\x11ListPostsResponse\x12\x19\n\x05posts\x18\x01 \x03(\x0b\x32\n.post.Post\x12\r\n\x05total\x18\x02 \x01(\x05\x12\x0c\n\x04page\x18\x03 \x01(\x05\x12\x10\n\x08per_page\x18\x04 \x01(\x05\x12\x11\n\tlast_page\x18\x05 \x01(\x05\x12\r\n\x05\x66rom_\x18\x06 \x01(\x05\x12\x0b\n\x03to_\x18\x07 \x01(\x05\"\x99\x01\n\x04Post\x12\x0f\n\x07post_id\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x12\n\ncreator_id\x18\x04 \x01(\t\x12\x12\n\ncreated_at\x18\x05 \x01(\t\x12\x12\n\nupdated_at\x18\x06 \x01(\t\x12\x12\n\nis_private\x18\x07 \x01(\x08\x12\x0c\n\x04tags\x18\x08 \x03(\t2\xc6\x02\n\x0bPostService\x12?\n\nCreatePost\x12\x17.post.CreatePostRequest\x1a\x18.post.CreatePostResponse\x12?\n\nDeletePost\x12\x17.post.DeletePostRequest\x1a\x18.post.DeletePostResponse\x12?\n\nUpdatePost\x12\x17.post.UpdatePostRequest\x1a\x18.post.UpdatePostResponse\x12\x36\n\x07GetPost\x12\x14.post.GetPostRequest\x1a\x15.post.GetPostResponse\x12<\n\tListPosts\x12\x16.post.ListPostsRequest\x1a\x17.post.ListPostsResponseb\x06proto3')



_CREATEPOSTREQUEST = DESCRIPTOR.message_types_by_name['CreatePostRequest']
_CREATEPOSTRESPONSE = DESCRIPTOR.message_types_by_name['CreatePostResponse']
_DELETEPOSTREQUEST = DESCRIPTOR.message_types_by_name['DeletePostRequest']
_DELETEPOSTRESPONSE = DESCRIPTOR.message_types_by_name['DeletePostResponse']
_UPDATEPOSTREQUEST = DESCRIPTOR.message_types_by_name['UpdatePostRequest']
_UPDATEPOSTRESPONSE = DESCRIPTOR.message_types_by_name['UpdatePostResponse']
_GETPOSTREQUEST = DESCRIPTOR.message_types_by_name['GetPostRequest']
_GETPOSTRESPONSE = DESCRIPTOR.message_types_by_name['GetPostResponse']
_LISTPOSTSREQUEST = DESCRIPTOR.message_types_by_name['ListPostsRequest']
_LISTPOSTSRESPONSE = DESCRIPTOR.message_types_by_name['ListPostsResponse']
_POST = DESCRIPTOR.message_types_by_name['Post']
CreatePostRequest = _reflection.GeneratedProtocolMessageType('CreatePostRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEPOSTREQUEST,
  '__module__' : 'proto.post_pb2'
  # @@protoc_insertion_point(class_scope:post.CreatePostRequest)
  })
_sym_db.RegisterMessage(CreatePostRequest)

CreatePostResponse = _reflection.GeneratedProtocolMessageType('CreatePostResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEPOSTRESPONSE,
  '__module__' : 'proto.post_pb2'
  # @@protoc_insertion_point(class_scope:post.CreatePostResponse)
  })
_sym_db.RegisterMessage(CreatePostResponse)

DeletePostRequest = _reflection.GeneratedProtocolMessageType('DeletePostRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEPOSTREQUEST,
  '__module__' : 'proto.post_pb2'
  # @@protoc_insertion_point(class_scope:post.DeletePostRequest)
  })
_sym_db.RegisterMessage(DeletePostRequest)

DeletePostResponse = _reflection.GeneratedProtocolMessageType('DeletePostResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETEPOSTRESPONSE,
  '__module__' : 'proto.post_pb2'
  # @@protoc_insertion_point(class_scope:post.DeletePostResponse)
  })
_sym_db.RegisterMessage(DeletePostResponse)

UpdatePostRequest = _reflection.GeneratedProtocolMessageType('UpdatePostRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEPOSTREQUEST,
  '__module__' : 'proto.post_pb2'
  # @@protoc_insertion_point(class_scope:post.UpdatePostRequest)
  })
_sym_db.RegisterMessage(UpdatePostRequest)

UpdatePostResponse = _reflection.GeneratedProtocolMessageType('UpdatePostResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEPOSTRESPONSE,
  '__module__' : 'proto.post_pb2'
  # @@protoc_insertion_point(class_scope:post.UpdatePostResponse)
  })
_sym_db.RegisterMessage(UpdatePostResponse)

GetPostRequest = _reflection.GeneratedProtocolMessageType('GetPostRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETPOSTREQUEST,
  '__module__' : 'proto.post_pb2'
  # @@protoc_insertion_point(class_scope:post.GetPostRequest)
  })
_sym_db.RegisterMessage(GetPostRequest)

GetPostResponse = _reflection.GeneratedProtocolMessageType('GetPostResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETPOSTRESPONSE,
  '__module__' : 'proto.post_pb2'
  # @@protoc_insertion_point(class_scope:post.GetPostResponse)
  })
_sym_db.RegisterMessage(GetPostResponse)

ListPostsRequest = _reflection.GeneratedProtocolMessageType('ListPostsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTPOSTSREQUEST,
  '__module__' : 'proto.post_pb2'
  # @@protoc_insertion_point(class_scope:post.ListPostsRequest)
  })
_sym_db.RegisterMessage(ListPostsRequest)

ListPostsResponse = _reflection.GeneratedProtocolMessageType('ListPostsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTPOSTSRESPONSE,
  '__module__' : 'proto.post_pb2'
  # @@protoc_insertion_point(class_scope:post.ListPostsResponse)
  })
_sym_db.RegisterMessage(ListPostsResponse)

Post = _reflection.GeneratedProtocolMessageType('Post', (_message.Message,), {
  'DESCRIPTOR' : _POST,
  '__module__' : 'proto.post_pb2'
  # @@protoc_insertion_point(class_scope:post.Post)
  })
_sym_db.RegisterMessage(Post)

_POSTSERVICE = DESCRIPTOR.services_by_name['PostService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CREATEPOSTREQUEST._serialized_start=26
  _CREATEPOSTREQUEST._serialized_end=135
  _CREATEPOSTRESPONSE._serialized_start=137
  _CREATEPOSTRESPONSE._serialized_end=194
  _DELETEPOSTREQUEST._serialized_start=196
  _DELETEPOSTREQUEST._serialized_end=249
  _DELETEPOSTRESPONSE._serialized_start=251
  _DELETEPOSTRESPONSE._serialized_end=288
  _UPDATEPOSTREQUEST._serialized_start=290
  _UPDATEPOSTREQUEST._serialized_end=413
  _UPDATEPOSTRESPONSE._serialized_start=415
  _UPDATEPOSTRESPONSE._serialized_end=455
  _GETPOSTREQUEST._serialized_start=457
  _GETPOSTREQUEST._serialized_end=507
  _GETPOSTRESPONSE._serialized_start=509
  _GETPOSTRESPONSE._serialized_end=552
  _LISTPOSTSREQUEST._serialized_start=554
  _LISTPOSTSREQUEST._serialized_end=621
  _LISTPOSTSRESPONSE._serialized_start=624
  _LISTPOSTSRESPONSE._serialized_end=764
  _POST._serialized_start=767
  _POST._serialized_end=920
  _POSTSERVICE._serialized_start=923
  _POSTSERVICE._serialized_end=1249
# @@protoc_insertion_point(module_scope)
