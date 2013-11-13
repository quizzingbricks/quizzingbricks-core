# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

import sqlalchemy as sa

from quizzingbricks.nuncius import NunciusService, expose
from quizzingbricks.common.db import session
from quizzingbricks.services.friends.models import Friendship
from quizzingbricks.services.users.models import User

from quizzingbricks.common.protocol import (
    protocol_mapper as p_mapper,
    protocol_inverse_mapper,
    RpcError,
    GetFriendsRequest,
    GetFriendsResponse,
    AddFriendRequest,
    AddFriendResponse,
    RemoveFriendRequest,
    RemoveFriendResponse

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

class FriendService(NunciusService):
    name = "friendservice"
    protocol_mapper = p_mapper
	
    @expose("add_friend")
    def add_friend(self, request):
        print "in add_Friend"
        with db(session):
            try:
                friend = User.query.filter(User.email==request.friend_email).first()
                friendship = Friendship(user_id = request.userId,
                                            friend_id = friend.id)
                session.add(friendship)
                session.commit()
                return AddFriendResponse(friend_added=True)           
            except Exception as e:
                session.rollback()
                return AddFriendResponse(friend_added=False)
                

    @expose("remove_friend")
    def remove_friend(self, request):
        print "in remove_friend"
        with db(session):
            try:
                friend = User.query.filter(User.email==request.friend_email).first()
                print friend.email
                print friend.id
                Friendship.query.filter(Friendship.friend_id==friend.id).delete()
                session.commit()
                return RemoveFriendResponse(friend_removed=True)
            except Exception as e:
                session.rollback()
                return RemoveFriendResponse(friend_removed=False)

    @expose("get_friends")
    def get_friends(self, request):
        with db(session):
            # NOTE: this fetch all friendships in the db
            # and is a "select N+1", change to something like this:
            # Friendship.query.filter(Friendship.user_id==request.userId) # fetch all friends by user
            # User.query.filter(User.id.in_(the above ids)) # fetch all users that matches the friendship ids
            # ... but can also be solved by a join.
            #
            # TODO: We may also decide if the user fetching should be done
            # by the user service which means that the friendservice calls the userservice over zmq via the client api
            # as planned earlier, but the responsible for this decide.
            friends = Friendship.query.filter()
            friend_list = []
            for friend in friends:
                friend_mail = User.query.get(friend.friend_id)
                friend_list.append(friend_mail.email)
            return GetFriendsResponse(friends_list=friend_list)
        
        
        # if (request.gameType == 4):
        #     return CreateLobbyResponse(lobbyId=123456)
        # if (request.gameType == 2):
        #     return CreateLobbyResponse(lobbyId=654321)
        # else:
        #     return CreateLobbyResponse(lobbyId=123321)

    

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