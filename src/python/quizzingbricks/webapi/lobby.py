# -*- coding: utf-8 -*-
"""
    Copyright (C) Quizzingbricks
"""

from flask import request, jsonify, g

from quizzingbricks.webapi import app, api_error, api_errors, token_required
from quizzingbricks.client.lobby import LobbyServiceClient
from quizzingbricks.client.exceptions import TimeoutError
from quizzingbricks.common.protocol import (
    RpcError, GetLobbyListRequest, GetLobbyListResponse,
    CreateLobbyRequest, CreateLobbyResponse, GetLobbyStateRequest, GetLobbyStateResponse,
    AnswerLobbyInviteRequest, InviteLobbyRequest, InviteLobbyResponse, StartGameRequest, RemoveLobbyRequest, RemoveLobbyResponse)

lobbyservice = LobbyServiceClient("tcp://*:5552")

@app.route("/api/games/lobby/", methods=["GET"])
@token_required
def get_lobbies():
    try:
        response = lobbyservice.get_lobbies(GetLobbyListRequest(userId=g.user.id), timeout=5000)

        lobbies_objects = [
            {
                "l_id": lobby.lobbyId,
                "owner": True if g.user.id == lobby.owner.id else False,
                "size": lobby.gameType,
                "invited_count": len(lobby.lobbymembers),
                "accepted_count": len(filter(lambda p: p.status == "member", lobby.lobbymembers))
            }
            for lobby in response.lobbies
        ]
        return jsonify(
            lobbies=lobbies_objects
        )
    except TimeoutError as e:
        return api_error("Service is not available", 500), 500
    except Exception as e:
        print "webapi#get_lobbies", e
        return api_error("Internal server error", 500), 500


@app.route("/api/games/lobby/", methods=["POST"])
@token_required
def create_lobby():
    try:
        game_size = request.form.get("size", type=int)
        if not game_size:
            return api_error("Missing required parameter size", 004), 400

        response = lobbyservice.create_lobby(CreateLobbyRequest(userId=g.user.id, gameType=game_size), timeout=5000)
        if not isinstance(response, CreateLobbyResponse): # maybe RpcError
            return api_error("Internal service error", 400), 400

        lobby_response = lobbyservice.get_lobby(GetLobbyStateRequest(lobbyId=response.lobbyId), timeout=5000)
        if not isinstance(lobby_response, GetLobbyStateResponse): # maybe RpcError
            return api_error("Internal service error", 400), 400

        lobby = lobby_response.lobby
        return jsonify(
            lobby={
                "l_id": lobby.lobbyId,
                "size": lobby.gameType,
                "owner": True if g.user.id == lobby.owner.id else False,
                "players": [
                    {"u_id": player.user.id, "u_mail": player.user.email, "status": "accepted" if player.status == "member" else "waiting"}
                    for player in list(lobby.lobbymembers)
                ]
            }
        )
    except TimeoutError as e:
        return api_error("Service is not available", 500), 500
    except Exception as e:
        return api_error("Internal server error", 500), 500


@app.route("/api/games/lobby/<int:id>/", methods=["GET"])
@token_required
def get_lobby(id):
    try:
        response = lobbyservice.get_lobby(GetLobbyStateRequest(lobbyId=id), timeout=5000)
        if isinstance(response, RpcError) and response.error_code == 2:
            return api_error("Lobby does not exists", 226), 404
        if not isinstance(response, GetLobbyStateResponse): # maybe RpcError
            return api_error("Internal service error", 400), 400

        lobby = response.lobby

        if not g.user.id in map(lambda m: m.user.id, lobby.lobbymembers):
            return api_error("You are not permitted to that lobby", 42), 400

        return jsonify(
            lobby={
                "l_id": lobby.lobbyId,
                "size": lobby.gameType,
                "owner": True if g.user.id == lobby.owner.id else False,
                "invited_count": len(lobby.lobbymembers),
                "accepted_count": len(filter(lambda p: p.status == "member", lobby.lobbymembers)),
                "players": [
                    {"u_id": player.user.id, "u_mail": player.user.email, "status": "accepted" if player.status == "member" else "waiting"}
                    for player in list(lobby.lobbymembers)
                ]
            }
        )
    except TimeoutError as e:
        return api_error("Service is not available", 500), 500


@app.route("/api/games/lobby/<int:lobby_id>/accept/", methods=["POST"])
@token_required
def accept_invite(lobby_id):
    try:
        response = lobbyservice.answer_lobby_invite(
            AnswerLobbyInviteRequest(userId=g.user.id, lobbyId=lobby_id, answer="accept")
        )
        if isinstance(response, RpcError):
            errors = {
                2: ({"message": "There exists no such lobby", "code": 226}, 404),
                30: ({"message": "You are not permitted to that lobby", "code": 42}, 400),
                31: ({"message": "The lobby is full", "code": 225}, 400),
            }
            error, status_code = errors.get(response.error_code)
            return api_error(**error), status_code
        return "OK" # TODO: fix real implementation according to spec when it's commented how it should be
    except TimeoutError as e:
        return api_error("Service not available", 500), 500


@app.route("/api/games/lobby/<int:lobby_id>/deny/", methods=["POST"])
@token_required
def deny_invite(lobby_id):
    try:
        response = lobbyservice.answer_lobby_invite(
            AnswerLobbyInviteRequest(userId=g.user.id, lobbyId=lobby_id, answer="deny")
        )
        if isinstance(response, RpcError):
            errors = {
                2: ({"message": "There exists no such lobby", "code": 226}, 404),
                30: ({"message": "You are not permitted to that lobby", "code": 42}, 400),
                31: ({"message": "The lobby is full", "code": 225}, 400),
            }
            error, status_code = errors.get(response.error_code)
            return api_error(**error), status_code
        return "OK" # TODO: fix real implementation according to spec when it's commented how it should be
    except TimeoutError as e:
        return api_error("Service not available", 500), 500


@app.route("/api/games/lobby/<int:lobby_id>/invite/", methods=["POST"])
@token_required
def lobby_invitation(lobby_id):
    try:
        if not request.json:
            return api_error("Required JSON body is missing or bad type, check your content-type")

        raw_user_ids = request.json.get("invite")
        if not raw_user_ids or not isinstance(raw_user_ids, list):
            return api_error("Required JSON body is missing or bad type", 004), 400
        user_ids = map(lambda x: int(x), raw_user_ids) # better method?


        response = lobbyservice.invite_to_lobby(
            InviteLobbyRequest(userId=g.user.id, lobbyId=lobby_id, invites=user_ids),
            timeout=5000
        )

        # TODO: return RpcError in the service
        #if isinstance(response, RpcError):
        #    pass

        if not isinstance(response, InviteLobbyResponse):
            return api_error("Internal service error")
        if response.friends_invited:
            return "OK"
        return "UNKNOWN INVITATION ERROR", 400

    except TimeoutError as e:
        return api_error("Service not available", 500), 500
    except ValueError as e:
        return  api_error("JSON object invite should be an array with only integers", 004), 400


@app.route("/api/games/lobby/<int:lobby_id>/start/", methods=["POST"])
@token_required
def start_lobby(lobby_id):
    try:
        response = lobbyservice.start_game(StartGameRequest(userId=g.user.id, lobbyId=lobby_id), timeout=5000)

        if isinstance(response, RpcError):
            if response.error_code == 2:
                return api_error("There exists no such lobby", 226), 404
            return api_error("You are not permitted to that lobby", 42), 400
        return "OK"
    except TimeoutError as e:
        return api_error("Service is not available", 500), 500

@app.route("/api/games/lobby/<int:lobby_id>/end/", methods=["POST"])
@token_required
def end_lobby(lobby_id):
    try:
        response = lobbyservice.remove_lobby(RemoveLobbyRequest(userId=g.user.id, lobbyId=lobby_id), timeout=5000)

        # TODO: add RpcError check!
        if isinstance(response, RemoveLobbyResponse):
            if response.lobby_removed: return "OK"
        return api_error("You are not permitted to that lobby", 42), 400 # assume until usage of RpcError
    except TimeoutError as e:
        return api_error("Service is not available", 500, 500)

