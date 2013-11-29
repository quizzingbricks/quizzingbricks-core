# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""
from quizzingbricks.client import BaseClient

class LobbyServiceClient(BaseClient):
    def getLobbyId(self, request, timeout=None):
        with self.rpc_call("get_lobby_id", request, timeout) as response:
            return response

    def getLobbyList(self, request, timeout=None):
        with self.rpc_call("get_lobby_list", request, timeout) as response:
            return response

    def getLobbyState(self, request, timeout=None):
        with self.rpc_call("get_lobby_state", request, timeout) as response:
            return response

    def answerLobbyInvite(self, request, timeout=None):
        with self.rpc_call("answer_lobby_invite", request, timeout) as response:
            return response

    def inviteToLobby(self, request, timeout=None):
        with self.rpc_call("invite_to_lobby", request, timeout) as response:
            return response

    def removeLobby(self, request, timeout=None):
        with self.rpc_call("remove_lobby", request, timeout) as response:
            return response
   
    def startGame(self, request, timeout=None):
        with self.rpc_call("start_game", request, timeout) as response:
            return response
            
    def createLobby(self, request, timeout=None):
        with self.rpc_call("create_lobby", request, timeout) as response:
            return response