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
    StartGameResponse,
    GetLobbyListRequest,
    GetLobbyListResponse,
    User as ProtoUser,
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
            return CreateLobbyResponse(lobbyId=123456)      #save gameType togther with the lobbyId
        if (request.gameType == 2):
            return CreateLobbyResponse(lobbyId=654321)
        else:
            return CreateLobbyResponse(lobbyId=123321)

    @expose("get_lobby_list")
    def get_lobby_list(self, request):
        print "get_lobby_list"
        #input : userId=1
        #return: lobbyIds =1, status=2 owner = 3 
        #used to get the status for a specific user in all the lobbies that the user is part off
        #status = Invited, Member
        #owner = userId of lobby owner
        test_lobby_1 = 123
        test_lobby_2 = 456
        test_lobby_3 = 789
        test_lobby_list = [test_lobby_1,test_lobby_2,test_lobby_3]
        test_lobby_1_status = "Member"
        test_lobby_2_status = "Invited"
        test_lobby_3_status = "Invited"
        status_list =[test_lobby_1_status, test_lobby_2_status, test_lobby_3_status]
        # test_lobby_1_owner = "Anton@test.se"
        # test_lobby_2_owner = "David@test.se"
        # test_lobby_3_owner = "Linus@test.se"
        test_owner_user_1  = ProtoUser(
                    id=11,
                    email="Anton@test.se",
                    username="Anton@test.se")

        test_owner_user_2  = ProtoUser(
                    id=22,
                    email="David@test.se",
                    username="David@test.se")

        test_owner_user_3  = ProtoUser(
                    id=33,
                    email="Linus@test.se",
                    username="Linus@test.se")

        # owner_list = [test_lobby_1_owner, test_lobby_2_owner, test_lobby_3_owner]
        test_owner_list = [test_owner_user_1, test_owner_user_2, test_owner_user_3]
        return GetLobbyListResponse(lobbyIds=test_lobby_list, status=status_list, owner=test_owner_list)


    @expose("get_lobby_state")
    def get_lobby_state(self, request):
        print "get_lobby_state"
        #input : lobbyId=1
        #return: friend_email=1, answer=2, gameType=3  
        #query with request.lobbyId
        # test_friend_1 = "Anton@test.se"
        # test_friend_2 = "David@test.se"
        # test_friend_3 = "Linus@test.se"
        # test_friend_list = [test_friend_1,test_friend_2,test_friend_3]
        test_user_1  = ProtoUser(
                    id=11,
                    email="Anton@test.se",
                    username="Anton@test.se")

        test_user_2  = ProtoUser(
                    id=22,
                    email="David@test.se",
                    username="David@test.se")

        test_user_3  = ProtoUser(
                    id=33,
                    email="Linus@test.se",
                    username="Linus@test.se")

        # owner_list = [test_lobby_1_owner, test_lobby_2_owner, test_lobby_3_owner]
        test_user_list = [test_user_1, test_user_2, test_user_3]
        test_friend_1_answer = "Accept"
        test_friend_2_answer = "Deny"
        test_friend_3_answer = "None"
        answer_list = [test_friend_1_answer,test_friend_2_answer,test_friend_3_answer]
        test_gameType = 2 
        return GetLobbyStateResponse(users=test_user_list, answer=answer_list, gameType=test_gameType)





    @expose("accept_lobby_invite")
    def accept_lobby_invite(self, request):
        print "accept_lobby_invite"
        #input : userId=1, lobbyId=2
        #return: answer=1
        #check user with request.userId and request.lobbyId also save answer in lobby state for this user
        return AcceptLobbyInviteResponse(answer="Accept")

    @expose("invite_to_lobby")
    def invite_to_lobby(self, request):
        print "invite_to_lobby"
        #input : userId=1, lobbyId=2, invite_emails=3
        #return: friends_invited =1
        #invite all the friends listed to lobbyId
        return InviteLobbyResponse(friends_invited=True)

    @expose("remove_lobby")
    def remove_lobby(self, request):
        print "remove_lobby"
        #input : userId=1, lobbyId=2
        #return: lobby_removed =1
        #removes the lobby
        return RemoveLobbyResponse(lobby_removed=True)

    @expose("start_game")
    def start_game(self, request):
        return StartGameResponse(isCreated=True)

    # @expose("start_game")         #Williams function suppose to be used
    # def start_game(self, request):
    #     if not isinstance(request, StartGameRequest):
    #        return RpcError(message="Wrong message type, expecting StartGameRequest")

    #     with db(session):
    #         if lobby.check_owner(request.userID): #TODO: this function
    #             # TODO send lobbyID to handlers addtoqueue
    #             return StartGameResponse(gameId=765432) #temporary test variable
    #     return RpcError(message="Incorrect user or lobby") 

