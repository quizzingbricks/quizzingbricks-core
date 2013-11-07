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
    CreateLobbyResponse
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

    

    # @expose("authenticate")
    # def authenticate_by_password(self, request):
    #     if not isinstance(request, LoginRequest):
    #         return RpcError(message="Wrong message type, expecting LoginRequest")
    #     with db(session):
    #         user = User.query.filter(User.email==request.email).first()
    #         if user and user.check_password(request.password):
    #             return LoginResponse(userId=user.id)
    #     return RpcError(message="Incorrect e-mail or password") # TODO: better method to handle error msgs?
    #     #if request.email == "demo@qb.se" and request.password == "demo":
    #     #    rep = LoginResponse()
    #     #    rep.userId = 123456
    #     #    return rep
    #     #return RpcError(message = "Incorrect e-mail or password")

    # @expose("authenticate_by_token")
    # def authenticate_by_token(self, request):
    #     pass

    # @expose("create_user")
    # def create_user(self, request):
    #     if not isinstance(request, RegistrationRequest):
    #         return RpcError(message = "Wrong message type, expecting RegistrationRequest")
    #     # TODO: add more logic before insert the user to db
    #     if None in (request.email, request.password):
    #         return RpcError(message="Both email and password requires to be set")
    #     try:
    #         user = User(
    #             email = request.email,
    #             password = request.password
    #         )
    #         session.add(user)
    #         session.commit()

    #         return RegistrationResponse(userId=user.id)
    #     except Exception as e:
    #         session.rollback()
    #         return RpcError(message=e.message) # TODO: improve this


    # @expose("get_user")
    # def get_user_by_id(self):
    #     pass