# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""
from quizzingbricks.client import BaseClient

class FriendServiceClient(BaseClient):
    def get_friends_list(self, request, timeout=None):
        with self.rpc_call("get_friends_list", request, timeout) as response:
            return response

    def add_friend(self, request, timeout=None):
        with self.rpc_call("add_friend", request, timeout) as response:
            return response

    def remove_friend(self, request, timeout=None):
        with self.rpc_call("remove_friend", request, timeout) as response:
            return response



   