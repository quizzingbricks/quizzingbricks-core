# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

import sqlalchemy as sa

from quizzingbricks.nuncius import NunciusService, expose
from quizzingbricks.common.db import session
from quizzingbricks.services.lobby.models import Lobby # .servives.lobby

from quizzingbricks.common.protocol import (
    protocol_mapper as p_mapper,
    protocol_inverse_mapper,
    RpcError,
    CreateLobbyRequest,
    CreateLobbyResponse,
    GetLobbyStateRequest,
    GetLobbyStateResponse,
    AcceptLobbyInviteRequest,
    AcceptLobbyInviteResponse,
    InviteLobbyRequest,
    InviteLobbyResponse,
    RemoveLobbyRequest,
    RemoveLobbyResponse,
    StartGameRequest,
    StartGameResponse
)

# TODO: add the type-checking in a decorator or directly in expose?

from contextlib import contextmanager

@contextmanager
def db(session):
    try:
        yield session
    finally:
        print "closed session"
        session.close()

class LobbyService(NunciusService):
    name = "lobbyservice"
    protocol_mapper = p_mapper

    @expose("get_lobby_id")
    def get_lobby_id(self, request):
        if (request.gameType == 4):
            return CreateLobbyResponse(lobbyId=123456)
        if (request.gameType == 2):
            return CreateLobbyResponse(lobbyId=654321)
        else:
            return CreateLobbyResponse(lobbyId=123321)


    @expose("get_lobby_state")
    def get_lobby_state(self, request):
        print "get_lobby_state"

    @expose("accept_lobby_invite")
    def accept_lobby_invite(self, request):
        print "accept_lobby_invite"

    @expose("invite_to_lobby")
    def invite_to_lobby(self, request):
        print "invite_to_lobby"

    @expose("remove_lobby")
    def remove_lobby(self, request):
        print "remove_lobby"

    @expose("start_game")
    def start_game(self, request):
        print "start_game"





