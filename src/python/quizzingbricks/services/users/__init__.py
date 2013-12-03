# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

import sqlalchemy as sa

from quizzingbricks.nuncius import NunciusService, expose
from quizzingbricks.common.db import session
from quizzingbricks.services.users.models import User

from quizzingbricks.common.protocol import (
    protocol_mapper as p_mapper,
    protocol_inverse_mapper,
    RpcError,
    User as ProtoUser,
    LoginRequest,
    LoginResponse,
    RegistrationRequest,
    RegistrationResponse,
    GetUserRequest,
    GetUserResponse,
    GetMultipleUsersRequest,
    GetMultipleUsersResponse

)

# TODO: add the type-checking in a decorator or directly in expose?

from contextlib import contextmanager
from sqlalchemy.exc import IntegrityError


@contextmanager
def db(session):
    try:
        yield session
    finally:
        print "closed session"
        session.remove()

class UserService(NunciusService):
    name = "userservice"
    protocol_mapper = p_mapper

    @expose("authenticate")
    def authenticate_by_password(self, request):
        if not isinstance(request, LoginRequest):
            return RpcError(message="Wrong message type, expecting LoginRequest", error_code=1)
        with db(session):
            user = User.query.filter(User.email==request.email).first()
            if user and user.check_password(request.password):
                return LoginResponse(userId=user.id)
        return RpcError(message="Incorrect e-mail or password", error_code=5) # TODO: better method to handle error msgs?
        #if request.email == "demo@qb.se" and request.password == "demo":
        #    rep = LoginResponse()
        #    rep.userId = 123456
        #    return rep
        #return RpcError(message = "Incorrect e-mail or password")


    @expose("create_user")
    def create_user(self, request):
        if not isinstance(request, RegistrationRequest):
            return RpcError(message = "Wrong message type, expecting RegistrationRequest", error_code=1)
        # TODO: add more logic before insert the user to db
        if None in (request.email, request.password):
            return RpcError(message="Both email and password requires to be set", error_code=10)
        try:
            user = User(
                email = request.email,
                password = request.password
            )
            session.add(user)
            session.commit()

            return RegistrationResponse(userId=user.id)
        except IntegrityError as e:
            session.rollback()
            return RpcError(message="E-mail already used", error_code=11)
        except Exception as e:
            session.rollback()
            return RpcError(message=e.message) # TODO: improve this


    @expose("get_user")
    def get_user_by_id(self, request):
        if not isinstance(request, GetUserRequest):
            return RpcError(message="Wrong message type, expecting GetUserRequest", error_code=1)

        with db(session):
            user = User.query.get(request.userId)
            if not user:
                return RpcError(message="No such user with id=%d" % request.userId)
            user_message = ProtoUser(
                id=user.id,
                email=user.email,
                username=user.email
            )
            return GetUserResponse(user=user_message)

    @expose("get_multiple_users")
    def get_multiple_users(self, request):
        if not isinstance(request, GetMultipleUsersRequest):
            return RpcError(message="Wrong message type, expecting GetUserRequest", error_code=1)

        with db(session):
            users = User.query.filter(User.id.in_(request.userIds))
            user_list=[]
            for user in users:
                user_message = ProtoUser(
                    id=user.id,
                    email=user.email,
                    username=user.email)
                user_list.append(user_message)
            return GetMultipleUsersResponse(users=user_list)