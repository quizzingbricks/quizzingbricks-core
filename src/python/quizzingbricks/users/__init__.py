# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

import sqlalchemy as sa

from quizzingbricks.nuncius import NunciusService, expose
from quizzingbricks.common.db import session
from quizzingbricks.users.models import User

from quizzingbricks.common.protocol import (
    protocol_mapper as p_mapper,
    protocol_inverse_mapper,
    RpcError,
    User as ProtoUser,
    LoginRequest,
    LoginResponse,
    RegistrationRequest,
    RegistrationResponse
)

class UserService(NunciusService):
    name = "userservice"
    protocol_mapper = p_mapper

    @expose("authenticate")
    def authenticate_by_password(self, request):
        if request.email == "demo@qb.se" and request.password == "demo":
            rep = LoginResponse()
            rep.userId = 123456
            return rep
        error = RpcError()
        error.message = "Incorrect e-mail or password"
        return error

    @expose("authenticate_by_token")
    def authenticate_by_token(self, request):
        pass

    @expose("create_user")
    def create_user(self, request):
        if not isinstance(request, RegistrationRequest):
            error = RpcError()
            error.message = "Wrong message type, expecting RegistrationRequest"
            return error
        # TODO: add more logic before insert the user to db
        user = User(
            email = request.email,
            password = request.password
        )
        session.add(user)
        session.commit()

        rep = RegistrationResponse()
        rep.userId = user.id

        return rep

    @expose("get_user")
    def get_user_by_id(self):
        pass