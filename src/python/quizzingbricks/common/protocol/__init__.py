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
    10: CreateGame,
    11: GameInfoRequest,
    12: GameInfoResponse,
    13: PlayerMove, 
    14: GameError
}

protocol_inverse_mapper = {v.__name__: k for k, v in protocol_mapper.iteritems()}
