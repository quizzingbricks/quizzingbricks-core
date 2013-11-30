# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""
from quizzingbricks.client import BaseClient

class LobbyServiceClient(BaseClient):
    def get_lobby_id(self, request, timeout=None):
        with self.rpc_call("get_lobby_id", request, timeout) as response:
            return response

    def get_lobbies(self, request, timeout=None):
        with self.rpc_call("get_lobby_list", request, timeout) as response:
            return response

    def get_lobby(self, request, timeout=None):
        with self.rpc_call("get_lobby_state", request, timeout) as response:
            return response

    def answer_lobby_invite(self, request, timeout=None):
        with self.rpc_call("answer_lobby_invite", request, timeout) as response:
            return response

    def invite_to_lobby(self, request, timeout=None):
        with self.rpc_call("invite_to_lobby", request, timeout) as response:
            return response

    def remove_lobby(self, request, timeout=None):
        with self.rpc_call("remove_lobby", request, timeout) as response:
            return response
   
    def start_game(self, request, timeout=None):
        with self.rpc_call("start_game", request, timeout) as response:
            return response
            
    def create_lobby(self, request, timeout=None):
        with self.rpc_call("create_lobby", request, timeout) as response:
            return response