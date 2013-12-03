# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

import sqlalchemy as sa
from quizzingbricks.services.lobby import lobbyqueue

from quizzingbricks.nuncius import NunciusService, expose
from quizzingbricks.common.db import session
from quizzingbricks.services.lobby.models import Lobby # .servives.lobby
from quizzingbricks.services.lobby.models import LobbyMembership
from quizzingbricks.services.users.models import User
from quizzingbricks.client.users import UserServiceClient



from quizzingbricks.common.protocol import (
    protocol_mapper as p_mapper,
    protocol_inverse_mapper,
    RpcError,
    CreateLobbyRequest,
    CreateLobbyResponse,
    GetLobbyStateRequest,
    GetLobbyStateResponse,
    AnswerLobbyInviteRequest,
    AnswerLobbyInviteResponse,
    InviteLobbyRequest,
    InviteLobbyResponse,
    RemoveLobbyRequest,
    RemoveLobbyResponse,
    StartGameRequest,
    StartGameResponse,
    GetLobbyListRequest,
    GetLobbyListResponse,
    GetMultipleUsersRequest,
    GetMultipleUsersResponse,
    GetUserRequest,
    GetUserResponse,
    LobbyMembership as ProtoLobbyMembership,
    Lobby as ProtoLobby
)


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
    
    @expose("create_lobby")
    def create_lobby(self, request):
        if not isinstance(request, CreateLobbyRequest):
            return RpcError(message="Wrong message type, expecting CreateLobbyRequest", error_code=1)
            
        lobby = Lobby(game_type = request.gameType, owner_id = request.userId)
        member = LobbyMembership(
            status="member",
            user_id=request.userId
        )
        lobby.lobbymemberships.append(member)

        session.add(lobby)
        session.commit()
        return CreateLobbyResponse(lobbyId=lobby.lobby_id)
            
    # TODO implement correctly if needed? Where is it used?        
    @expose("get_lobby_id")
    def get_lobby_id(self, request):
        print "get_lobby_id"      
        lobby_query = Lobby.query.filter(Lobby.owner_id==request.userId).all()
        lobby_ids = map(lambda l:l.lobby_id, lobby_query)
        
        return CreateLobbyResponse(lobbyId=lobby_ids[0])

    @expose("get_lobby_list_helper")
    def get_lobby_list_helper(self, lobbyid, lobby, isid):
        if(lobbyid == lobby.lobby_id):
            
            if(isid):
                return lobby.user_id
            return lobby.status
            
    @expose("get_lobby_list")
    def get_lobby_list(self, request):
        with db(session):
            userservice = UserServiceClient("tcp://*:5551")
            # Get all the lobbies that the user with userId is in
            lobbyMembershipQuery = LobbyMembership.query.filter(LobbyMembership.user_id==request.userId).all()
            
            if(lobbyMembershipQuery == []):
                return GetLobbyListResponse(lobbies=[])
            else:
                lobbies_list = [] # List for lobbies to be returned
                for lobby in lobbyMembershipQuery:
                    # Get the owner_id and game_type of the lobby
                    lobbyQuery = Lobby.query.filter(Lobby.lobby_id==lobby.lobby_id).first()
                    lobby_owner=userservice.get_user(GetUserRequest(userId=lobbyQuery.owner_id), timeout=5000)
                    # Get all the players that are in the lobby
                    lobbyMembersQuery = LobbyMembership.query.filter(LobbyMembership.lobby_id==lobby.lobby_id).all()
                    lobbymemb_list = [] # List for lobby memberships for the inner loop
                    for member in lobbyMembersQuery:
                        # Create lobby membership
                        user_request=userservice.get_user(GetUserRequest(userId=member.user_id), timeout=5000)
                        the_actual_user = user_request.user
                        lobbym = ProtoLobbyMembership(user=the_actual_user, status=member.status) 
                        lobbymemb_list.append(lobbym) 
                    
                    lobby_i = ProtoLobby(lobbyId=lobby.lobby_id, owner=lobby_owner.user, lobbymembers=lobbymemb_list, gameType=lobbyQuery.game_type) # Create lobby
                    lobbies_list.append(lobby_i) # Append lobby to return list
                return GetLobbyListResponse(lobbies=lobbies_list)
    """
        if not isinstance(request, GetLobbyListRequest):
            return RpcError(message="Wrong message type, expecting GetLobbyListRequest", error_code=1)    
        
        with db(session):
            users = {}
            lobbyMembershipQuery = LobbyMembership.query.filter(LobbyMembership.user_id==request.userId).all()
            + joinedload (Lobby)
            + joinedload (members)
            
            all_members = all members ids
            
            GetMultipleUserReq(all_members) -> users[id] = user
            
            for l in lobbies:
                x = Lobby()
                for y in l.players:
                    x.player.append(users.get(y.user_id))
                    
            
        
            userservice = UserServiceClient("tcp://*:5551")
            # Get all the lobbies that the user with userId is in
            lobbyMembershipQuery = LobbyMembership.query.filter(LobbyMembership.user_id==request.userId).all()
            lobbies = map(lambda i:i.lobby_id, lobbyMembershipQuery)
            
            if(lobbyMembershipQuery == []):
                return GetLobbyListResponse(lobbies=[])
            else:
                lobbies_list = [] # List for lobbies to be returned
                # Get the owners of the lobbies as users
                lobbyQuery = Lobby.query.filter(Lobby.lobby_id.in_(lobbies)).all()
                owners = map(lambda i:i.owner_id, lobbyQuery)
                lobby_owner=userservice.get_user(GetMultipleUsersRequest(userIds=owners), timeout=5000)
                # Get the game types
                game_types = map(lambda i:i.game_type, lobbyQuery)
                # Get lobbymembers
                lobbyMembersQuery = LobbyMembership.query.filter(LobbyMembership.lobby_id.in_(lobbies)).all()
                
                
                for lobby in lobbies:
                    members_id = map(lambda i: i.user_id if i.lobby_id==lobby else None, lobbyMembersQuery)
                    lobby_members = userservice.get_user(GetMultipleUsersRequest(userIds=members_id), timeout=5000)
                    users_map = lobby_members.users
                    members_status = map(lambda i: i.status if i.lobby_id==lobby else None, lobbyMembersQuery)
                    
                    lobbym_list = []
                    for memb in members_id:
                        users_map = lobby_members.users.pop()
                        status = members_status.pop()
                        lobbym = ProtoLobbyMembership(user=user, status=status)
                        lobbym_list.append(lobbym)

                    create_lobby = Lobby(lobbyId=lobby.lobby_id, owner=owners.pop(), lobbymembers=lobbym_list, gameType=game_types.pop())
                    lobbies_list.append(create_lobby)
                return GetLobbyListResponse(lobbies=lobbies_list)
"""


    @expose("get_lobby_state")
    def get_lobby_state(self, request):
        if not isinstance(request, GetLobbyStateRequest):
            return RpcError(message="Wrong message type, expecting GetLobbyStateRequest", error_code=1)         
       
        with db(session):
            userservice = UserServiceClient("tcp://*:5551")
            lobbyQuery = Lobby.query.filter(Lobby.lobby_id==request.lobbyId).first()
            if not lobbyQuery:
                return RpcError(message="Lobby does not exists", error_code=2)
            lobbyMembershipQuery = LobbyMembership.query.filter(LobbyMembership.lobby_id==request.lobbyId).all()
            lobbyOwner = userservice.get_user(GetUserRequest(userId=lobbyQuery.owner_id), timeout=5000)
            
            lobbymemb_list = []
            for member in lobbyMembershipQuery:
                userInLobby = userservice.get_user(GetUserRequest(userId=member.user_id), timeout=5000)
                lobbym = ProtoLobbyMembership(user=userInLobby.user, status=member.status) 
                lobbymemb_list.append(lobbym)
                print "the user", userInLobby.user.email
                print "status", member.status
            
            lobby_return = ProtoLobby(lobbyId=request.lobbyId, owner=lobbyOwner.user, lobbymembers=lobbymemb_list, gameType=lobbyQuery.game_type) # Create lobby
                    
            return GetLobbyStateResponse(lobby=lobby_return)


    @expose("answer_lobby_invite")
    def answer_lobby_invite(self, request):
        if not isinstance(request, AnswerLobbyInviteRequest):
            return RpcError(message="Wrong message type, expecting AnswerLobbyInviteRequest", error_code=1)
            
        with db(session):
            query_type = Lobby.query.filter(Lobby.lobby_id==request.lobbyId).first()
            if not query_type:
                return RpcError(message="Lobby does not exists", error_code=2)
            accepted_count = LobbyMembership.query.filter(LobbyMembership.lobby_id==request.lobbyId).filter(LobbyMembership.status=="member").count()

            user_lobby = LobbyMembership.query.filter(LobbyMembership.lobby_id==request.lobbyId).filter(LobbyMembership.user_id==request.userId).first()
            if not user_lobby:
                return RpcError(message="Not permitted to the lobby", error_code=30)

            if(request.answer == "accept"):
                if(query_type.game_type >= accepted_count + 1):
                    session.delete(user_lobby)
                    session.add(LobbyMembership(lobby_id=user_lobby.lobby_id, status="member", user_id=user_lobby.user_id))
                    session.commit()
                    return AnswerLobbyInviteResponse(answer=True)
                else:
                    session.delete(user_lobby)
                    session.commit()
                    return RpcError(message="Lobby is full", error_code=31)
                    
            elif(request.answer == "deny"):
                try:
                    session.delete(user_lobby)
                    session.commit()
                    return AnswerLobbyInviteResponse(answer=True)
            
                except Exception as e:
                    return AnswerLobbyInviteResponse(answer=False)
            
            return RpcError(message="Unknown answer should be accept or deny", error_code=3)

     

    @expose("invite_to_lobby")
    def invite_to_lobby(self, request):
        if not isinstance(request, InviteLobbyRequest):
            return RpcError(message="Wrong message type, expecting InviteLobbyRequest", error_code=1)
            
        if not request.invites:
            return InviteLobbyResponse(friends_invited=False)

        with db(session):
            lobby = Lobby.query.filter(Lobby.lobby_id==request.lobbyId).filter(Lobby.owner_id==request.userId).first()
            if(lobby==None):
                return RpcError(message="No permission to manage the lobby", error_code=35)
                
            # Clearing out duplicates from invited list
            users = User.query.filter(User.id.in_(request.invites)).all()
            users = set(users)
            uids = map(lambda u:u.id, users)
            
            # Check to make sure the lobby owner does not get invited
            for user in users:
                if(user.id == request.userId):
                    users.remove(user)
                    break
            
            # Check and remove invited users who has previously been invited
            already_invited = LobbyMembership.query.filter(LobbyMembership.user_id.in_(uids)).filter(LobbyMembership.lobby_id==request.lobbyId).all()
            for invited in already_invited:
                for person in users:
                    if(invited.user_id==person.id):
                        users.remove(person)
                        break
                    
                    
            print users
            if(users == set([])):
                return InviteLobbyResponse(friends_invited=False)
            
            else:
                for invited in users:
                    lobby_membership = LobbyMembership(lobby_id = request.lobbyId, status = "invited" , user_id = invited.id)
                    session.add(lobby_membership)
                
                session.commit()               
                return InviteLobbyResponse(friends_invited=True)   
                

    @expose("remove_lobby")
    def remove_lobby(self, request):
        if not isinstance(request, RemoveLobbyRequest):
            return RpcError(message="Wrong message type, expecting RemoveLobbyRequest", error_code=1)
        
        try:
            with db(session):
                # Delete from Lobby table
                lobby = Lobby.query.filter(Lobby.lobby_id==request.lobbyId).filter(Lobby.owner_id==request.userId).first()
                if(lobby==None):
                    return RpcError(message="No permission to manage the lobby", error_code=35)
                session.delete(lobby)
            
                # Delete from LobbyMembership
                lobby_membership = LobbyMembership.query.filter(LobbyMembership.lobby_id==request.lobbyId).all()
                for member in lobby_membership:
                    session.delete(member)
                
                session.commit()
                return RemoveLobbyResponse(lobby_removed=True)
                
        except Exception as e:
            return RemoveLobbyResponse(lobby_removed=False)
        

    @expose("start_game")
    def start_game(self, request):
        if not isinstance(request, StartGameRequest):
            return RpcError(message="Wrong message type, expecting StartGameRequest", error_code=1)

        with db(session):
            lobbyQuery = Lobby.query.filter(Lobby.lobby_id==request.lobbyId).first()

            if not lobbyQuery:
                return RpcError(message="Lobby does not exists", error_code=002)

            if lobbyQuery.owner_id == request.userId:
                lobbyMembershipQuery = LobbyMembership.query.filter(LobbyMembership.lobby_id == request.lobbyId).filter(LobbyMembership.status=="member").all()
                users = map(lambda i:i.user_id, lobbyMembershipQuery)
                
                # TODO send lobbyID to handlers addtoqueue
                lobbyqueue.addtoqueue(request.lobbyId, lobbyQuery.game_type, users)
                lobbyqueue.worker()
                
                
                
                # remove lobby from database
                removed = self.remove_lobby(RemoveLobbyRequest(userId=request.userId, lobbyId=request.lobbyId))
                
                if removed.lobby_removed:
                    return StartGameResponse(isCreated=True) #temporary test variable
                else:
                    return StartGameResponse(isCreated=False)
        return RpcError(message="No permission to manage the lobby", error_code=35)

