# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""
from quizzingbricks.client import BaseClient

class LobbyServiceClient(BaseClient):
    def getLobbyId(self, request, timeout=None):
        with self.rpc_call("get_Lobby_Id", request, timeout) as response:
            return response

   