# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

import sqlalchemy as sa

from quizzingbricks.nuncius import NunciusService, expose
from quizzingbricks.common.db import session
from quizzingbricks.services.friends.models import FriendsList

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
        # Query database to make sure friend is a user and if it is add it to friends list
        if(True):   #switch to query test
            return AddFriendResponse(friend_added=True)
        else:
            return AddFriendResponse(friend_added=False)

    @expose("remove_friend")
    def remove_friend(self, request):
        print "in remove_friend"
        # Query database to make sure friend is a user and if it is add it to friends list
        if(True):   #switch to query test
            return RemoveFriendResponse(friend_removed=True)
        else:
            return RemoveFriendResponse(friend_removed=False)

    @expose("get_friends_list")
    def get_friends_list(self, request):
        test_friend_1 = "Anton@test.se"
        test_friend_2 = "David@test.se"
        test_friend_3 = "Linus@test.se"
        test_friend_4 = "William@test.se" 
        test_friend_5 = "Niklas@test.se"
        test_friends_list=[test_friend_1,test_friend_2,test_friend_3,test_friend_4,test_friend_5]
        return GetFriendsResponse(friends_list=test_friends_list)
 