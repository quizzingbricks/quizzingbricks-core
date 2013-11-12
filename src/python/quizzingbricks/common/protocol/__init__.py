# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

# hack to make all visible under quizzingbricks.common.protocol.*
from protocol_pb2 import *
from base_pb2 import *
from users_pb2 import *
from lobbies_pb2 import *
from friends_pb2 import *
from games_pb2 import *

protocol_mapper = {
    1: RpcError,
    2: LoginRequest,
    3: LoginResponse,
    4: RegistrationRequest,
    5: RegistrationResponse,
    6: CreateLobbyRequest,
    7: CreateLobbyResponse,
    8: GetFriendsRequest,
    9: GetFriendsResponse,
    10: CreateGameRequest,
    11: GameInfoRequest,
    12: GameInfoResponse,
    13: MoveRequest, 
    14: GameError,
    15: AddFriendRequest,
    16: AddFriendResponse,
    17: RemoveFriendRequest,
    18: RemoveFriendResponse,
    19: GetUserRequest,
    20: GetUserResponse,
    21: GetLobbyStateRequest,
    22: GetLobbyStateResponse,
    23: AcceptLobbyInviteRequest,
    24: AcceptLobbyInviteResponse,
    25: InviteLobbyRequest,
    26: InviteLobbyResponse,
    27: RemoveLobbyRequest,
    28: RemoveLobbyResponse,
    29: StartGameRequest,
    30: StartGameResponse,
    31: QuestionRequest,
    32: QuestionResponse,
    33: AnswerRequest,
    34: AnswerResponse,
    35: MoveResponse,
    36: CreateGameResponse,
    37: GetLobbyListRequest,
    38: GetLobbyListResponse
}

protocol_inverse_mapper = {v.__name__: k for k, v in protocol_mapper.iteritems()}
