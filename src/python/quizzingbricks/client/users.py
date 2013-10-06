# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""
from quizzingbricks.client import BaseClient

class UserClient(BaseClient):
    def authenticate(self, request, timeout=None):
        with self.rpc_call("authenticate", request, timeout) as response:
            return response
