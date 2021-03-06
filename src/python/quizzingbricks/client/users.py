# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""
from quizzingbricks.client import BaseClient

class UserServiceClient(BaseClient):
    def authenticate(self, request, timeout=None):
        with self.rpc_call("authenticate", request, timeout) as response:
            return response

    def create_user(self, request, timeout=None):
        with self.rpc_call("create_user", request, timeout) as response:
            return response

    def get_user(self, request, timeout=None):
        with self.rpc_call("get_user", request, timeout) as response:
            return response

    def get_multiple_users(self, request, timeout=None):
        with self.rpc_call("get_multiple_users", request, timeout) as response:
            return response
