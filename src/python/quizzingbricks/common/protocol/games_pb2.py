# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: games.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='games.proto',
  package='',
  serialized_pb='\n\x0bgames.proto\"$\n\x11\x43reateGameRequest\x12\x0f\n\x07players\x18\x01 \x03(\x05\"$\n\x12\x43reateGameResponse\x12\x0e\n\x06gameId\x18\x01 \x02(\x05\"?\n\x04Game\x12\x0e\n\x06gameId\x18\x01 \x02(\x05\x12\x18\n\x07players\x18\x02 \x03(\x0b\x32\x07.Player\x12\r\n\x05\x62oard\x18\x03 \x03(\x05\"!\n\x0fGameInfoRequest\x12\x0e\n\x06gameId\x18\x01 \x02(\x05\"\'\n\x10GameInfoResponse\x12\x13\n\x04game\x18\x01 \x02(\x0b\x32\x05.Game\"!\n\x0fGameListRequest\x12\x0e\n\x06userId\x18\x01 \x02(\x05\"(\n\x10GameListResponse\x12\x14\n\x05games\x18\x01 \x03(\x0b\x32\x05.Game\"\x80\x01\n\x06Player\x12\x0e\n\x06userId\x18\x01 \x02(\x05\x12\r\n\x05state\x18\x02 \x02(\x05\x12\t\n\x01x\x18\x03 \x01(\x05\x12\t\n\x01y\x18\x04 \x01(\x05\x12\x10\n\x08question\x18\x05 \x01(\t\x12\x14\n\x0c\x61lternatives\x18\x06 \x03(\t\x12\x19\n\x11\x61nsweredCorrectly\x18\x07 \x01(\x08\"C\n\x0bMoveRequest\x12\x0e\n\x06gameId\x18\x01 \x02(\x05\x12\x0e\n\x06userId\x18\x02 \x02(\x05\x12\t\n\x01x\x18\x03 \x02(\x05\x12\t\n\x01y\x18\x04 \x02(\x05\"\x0e\n\x0cMoveResponse\"1\n\x0fQuestionRequest\x12\x0e\n\x06gameId\x18\x01 \x02(\x05\x12\x0e\n\x06userId\x18\x02 \x02(\x05\":\n\x10QuestionResponse\x12\x10\n\x08question\x18\x01 \x02(\t\x12\x14\n\x0c\x61lternatives\x18\x02 \x03(\t\"?\n\rAnswerRequest\x12\x0e\n\x06gameId\x18\x01 \x02(\x05\x12\x0e\n\x06userId\x18\x02 \x02(\x05\x12\x0e\n\x06\x61nswer\x18\x03 \x02(\x05\"#\n\x0e\x41nswerResponse\x12\x11\n\tisCorrect\x18\x01 \x02(\x08\"X\n\tGameError\x12\x13\n\x0b\x64\x65scription\x18\x01 \x02(\t\x12\x0c\n\x04\x63ode\x18\x02 \x02(\x05\x12(\n\rgameinforeply\x18\x03 \x01(\x0b\x32\x11.GameInfoResponse\"/\n\x18\x42oardChangePubSubMessage\x12\x13\n\x04game\x18\x01 \x02(\x0b\x32\x05.Game\"\x17\n\x15NewRoundPubSubMessageB\x0e\x42\x0cGameprotocol')




_CREATEGAMEREQUEST = _descriptor.Descriptor(
  name='CreateGameRequest',
  full_name='CreateGameRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='players', full_name='CreateGameRequest.players', index=0,
      number=1, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=15,
  serialized_end=51,
)


_CREATEGAMERESPONSE = _descriptor.Descriptor(
  name='CreateGameResponse',
  full_name='CreateGameResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='gameId', full_name='CreateGameResponse.gameId', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=53,
  serialized_end=89,
)


_GAME = _descriptor.Descriptor(
  name='Game',
  full_name='Game',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='gameId', full_name='Game.gameId', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='players', full_name='Game.players', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='board', full_name='Game.board', index=2,
      number=3, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=91,
  serialized_end=154,
)


_GAMEINFOREQUEST = _descriptor.Descriptor(
  name='GameInfoRequest',
  full_name='GameInfoRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='gameId', full_name='GameInfoRequest.gameId', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=156,
  serialized_end=189,
)


_GAMEINFORESPONSE = _descriptor.Descriptor(
  name='GameInfoResponse',
  full_name='GameInfoResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='game', full_name='GameInfoResponse.game', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=191,
  serialized_end=230,
)


_GAMELISTREQUEST = _descriptor.Descriptor(
  name='GameListRequest',
  full_name='GameListRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='userId', full_name='GameListRequest.userId', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=232,
  serialized_end=265,
)


_GAMELISTRESPONSE = _descriptor.Descriptor(
  name='GameListResponse',
  full_name='GameListResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='games', full_name='GameListResponse.games', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=267,
  serialized_end=307,
)


_PLAYER = _descriptor.Descriptor(
  name='Player',
  full_name='Player',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='userId', full_name='Player.userId', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='state', full_name='Player.state', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='x', full_name='Player.x', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='Player.y', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='question', full_name='Player.question', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='alternatives', full_name='Player.alternatives', index=5,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='answeredCorrectly', full_name='Player.answeredCorrectly', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=310,
  serialized_end=438,
)


_MOVEREQUEST = _descriptor.Descriptor(
  name='MoveRequest',
  full_name='MoveRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='gameId', full_name='MoveRequest.gameId', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='userId', full_name='MoveRequest.userId', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='x', full_name='MoveRequest.x', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='MoveRequest.y', index=3,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=440,
  serialized_end=507,
)


_MOVERESPONSE = _descriptor.Descriptor(
  name='MoveResponse',
  full_name='MoveResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=509,
  serialized_end=523,
)


_QUESTIONREQUEST = _descriptor.Descriptor(
  name='QuestionRequest',
  full_name='QuestionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='gameId', full_name='QuestionRequest.gameId', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='userId', full_name='QuestionRequest.userId', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=525,
  serialized_end=574,
)


_QUESTIONRESPONSE = _descriptor.Descriptor(
  name='QuestionResponse',
  full_name='QuestionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='question', full_name='QuestionResponse.question', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='alternatives', full_name='QuestionResponse.alternatives', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=576,
  serialized_end=634,
)


_ANSWERREQUEST = _descriptor.Descriptor(
  name='AnswerRequest',
  full_name='AnswerRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='gameId', full_name='AnswerRequest.gameId', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='userId', full_name='AnswerRequest.userId', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='answer', full_name='AnswerRequest.answer', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=636,
  serialized_end=699,
)


_ANSWERRESPONSE = _descriptor.Descriptor(
  name='AnswerResponse',
  full_name='AnswerResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='isCorrect', full_name='AnswerResponse.isCorrect', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=701,
  serialized_end=736,
)


_GAMEERROR = _descriptor.Descriptor(
  name='GameError',
  full_name='GameError',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='description', full_name='GameError.description', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='code', full_name='GameError.code', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gameinforeply', full_name='GameError.gameinforeply', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=738,
  serialized_end=826,
)


_BOARDCHANGEPUBSUBMESSAGE = _descriptor.Descriptor(
  name='BoardChangePubSubMessage',
  full_name='BoardChangePubSubMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='game', full_name='BoardChangePubSubMessage.game', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=828,
  serialized_end=875,
)


_NEWROUNDPUBSUBMESSAGE = _descriptor.Descriptor(
  name='NewRoundPubSubMessage',
  full_name='NewRoundPubSubMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=877,
  serialized_end=900,
)

_GAME.fields_by_name['players'].message_type = _PLAYER
_GAMEINFORESPONSE.fields_by_name['game'].message_type = _GAME
_GAMELISTRESPONSE.fields_by_name['games'].message_type = _GAME
_GAMEERROR.fields_by_name['gameinforeply'].message_type = _GAMEINFORESPONSE
_BOARDCHANGEPUBSUBMESSAGE.fields_by_name['game'].message_type = _GAME
DESCRIPTOR.message_types_by_name['CreateGameRequest'] = _CREATEGAMEREQUEST
DESCRIPTOR.message_types_by_name['CreateGameResponse'] = _CREATEGAMERESPONSE
DESCRIPTOR.message_types_by_name['Game'] = _GAME
DESCRIPTOR.message_types_by_name['GameInfoRequest'] = _GAMEINFOREQUEST
DESCRIPTOR.message_types_by_name['GameInfoResponse'] = _GAMEINFORESPONSE
DESCRIPTOR.message_types_by_name['GameListRequest'] = _GAMELISTREQUEST
DESCRIPTOR.message_types_by_name['GameListResponse'] = _GAMELISTRESPONSE
DESCRIPTOR.message_types_by_name['Player'] = _PLAYER
DESCRIPTOR.message_types_by_name['MoveRequest'] = _MOVEREQUEST
DESCRIPTOR.message_types_by_name['MoveResponse'] = _MOVERESPONSE
DESCRIPTOR.message_types_by_name['QuestionRequest'] = _QUESTIONREQUEST
DESCRIPTOR.message_types_by_name['QuestionResponse'] = _QUESTIONRESPONSE
DESCRIPTOR.message_types_by_name['AnswerRequest'] = _ANSWERREQUEST
DESCRIPTOR.message_types_by_name['AnswerResponse'] = _ANSWERRESPONSE
DESCRIPTOR.message_types_by_name['GameError'] = _GAMEERROR
DESCRIPTOR.message_types_by_name['BoardChangePubSubMessage'] = _BOARDCHANGEPUBSUBMESSAGE
DESCRIPTOR.message_types_by_name['NewRoundPubSubMessage'] = _NEWROUNDPUBSUBMESSAGE

class CreateGameRequest(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CREATEGAMEREQUEST

  # @@protoc_insertion_point(class_scope:CreateGameRequest)

class CreateGameResponse(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CREATEGAMERESPONSE

  # @@protoc_insertion_point(class_scope:CreateGameResponse)

class Game(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GAME

  # @@protoc_insertion_point(class_scope:Game)

class GameInfoRequest(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GAMEINFOREQUEST

  # @@protoc_insertion_point(class_scope:GameInfoRequest)

class GameInfoResponse(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GAMEINFORESPONSE

  # @@protoc_insertion_point(class_scope:GameInfoResponse)

class GameListRequest(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GAMELISTREQUEST

  # @@protoc_insertion_point(class_scope:GameListRequest)

class GameListResponse(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GAMELISTRESPONSE

  # @@protoc_insertion_point(class_scope:GameListResponse)

class Player(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PLAYER

  # @@protoc_insertion_point(class_scope:Player)

class MoveRequest(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _MOVEREQUEST

  # @@protoc_insertion_point(class_scope:MoveRequest)

class MoveResponse(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _MOVERESPONSE

  # @@protoc_insertion_point(class_scope:MoveResponse)

class QuestionRequest(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _QUESTIONREQUEST

  # @@protoc_insertion_point(class_scope:QuestionRequest)

class QuestionResponse(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _QUESTIONRESPONSE

  # @@protoc_insertion_point(class_scope:QuestionResponse)

class AnswerRequest(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ANSWERREQUEST

  # @@protoc_insertion_point(class_scope:AnswerRequest)

class AnswerResponse(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ANSWERRESPONSE

  # @@protoc_insertion_point(class_scope:AnswerResponse)

class GameError(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GAMEERROR

  # @@protoc_insertion_point(class_scope:GameError)

class BoardChangePubSubMessage(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BOARDCHANGEPUBSUBMESSAGE

  # @@protoc_insertion_point(class_scope:BoardChangePubSubMessage)

class NewRoundPubSubMessage(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _NEWROUNDPUBSUBMESSAGE

  # @@protoc_insertion_point(class_scope:NewRoundPubSubMessage)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), 'B\014Gameprotocol')
# @@protoc_insertion_point(module_scope)
