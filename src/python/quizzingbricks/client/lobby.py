# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""
from quizzingbricks.client import BaseClient

class LobbyServiceClient(BaseClient):
    def getLobbyId(self, request, timeout=None):
        with self.rpc_call("authenticate", request, timeout) as response:
            return response

   