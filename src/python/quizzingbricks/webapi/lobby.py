# -*- coding: utf-8 -*-
"""
    Copyright (C) Quizzingbricks
"""

from flask import request, jsonify, g

from quizzingbricks.webapi import app, api_error, api_errors, token_required
from quizzingbricks.client.lobby import LobbyServiceClient
from quizzingbricks.client.exceptions import TimeoutError
from quizzingbricks.common.protocol import (
    GetLobbyListRequest, GetLobbyListResponse,
    RpcError)

lobbyservice = LobbyServiceClient("tcp://*:5551")

@app.route("/api/games/lobby/")
@token_required
def get_lobbies():
    try:
        lobbies = lobbyservice.get_lobbies(GetLobbyListRequest(userId=g.user.id), timeout=5000)

        lobbies_objects = [{} for lobby in lobbies]
    except TimeoutError as e:
        pass
