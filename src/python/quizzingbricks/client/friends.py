# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""
from quizzingbricks.client import BaseClient

class FriendServiceClient(BaseClient):
    def get_Friends_list(self, request, timeout=None):
        with self.rpc_call("get_Friends_List", request, timeout) as response:
            return response

    def add_Friend(self, request, timeout=None):
        with self.rpc_call("add_Friend", request, timeout) as response:
            return response

    def remove_Friend(self, request, timeout=None):
        with self.rpc_call("remove_Friend", request, timeout) as response:
            return response



   