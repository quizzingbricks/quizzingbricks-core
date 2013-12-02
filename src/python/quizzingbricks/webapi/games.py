# -*- coding: utf-8 -*-
"""
    Copyright (C) Quizzingbricks
"""
import random

import sys, traceback
import json
from flask import request, jsonify, g, abort
import zmq.green as zmq

from quizzingbricks.webapi import app, api_error, api_errors, token_required, zmq_ctx
from quizzingbricks.client.games import GameServiceClient
from quizzingbricks.client.exceptions import TimeoutError

from quizzingbricks.common.protocol import (
    GameError, GameInfoRequest, GameInfoResponse,
    MoveRequest,
    QuestionRequest, AnswerRequest,
    BoardChangePubSubMessage, NewRoundPubSubMessage, GameListRequest)
from quizzingbricks.common.protocol import protocol_mapper

gameservice = GameServiceClient("tcp://*:1234", zmq_context=zmq_ctx)

@app.route("/api/games/", methods=["GET"])
@token_required
def list_games():
    try:
        response = gameservice.send(GameListRequest(userId=g.user.id), timeout=5000)
        if isinstance(response, GameError):
            return api_error(response.description, response.code), 400
        return jsonify(games=[
            game.gameId for game in list(response.games)
        ])

    except TimeoutError as e:
        return api_error("Service is not available", 500), 500


@app.route("/api/games/<int:game_id>/", methods=["GET"])
@token_required
def game_details(game_id):
    msg = GameInfoRequest(gameId=game_id)

    try:
        rep = gameservice.send(msg, timeout=5000)
        if isinstance(rep, GameError):
            return api_error(rep.description, rep.code), 400
        else:
            return jsonify({ "gameId" : rep.game.gameId,
                             "players" : [ { "userId" : player.userId,
                                            "state" : player.state,
                                            "x" : player.x,
                                            "y" : player.y,
                                            "score": player.score,
                                            #"question" : player.question,
                                            #"alternatives" : [a for a in player.alternatives],
                                            "answeredCorrectly" : player.answeredCorrectly } for player in rep.game.players ],
                             "board" : [ b for b in rep.game.board ]
                          })
    except TimeoutError as e:
        return api_error("Game service not available", 500)

@app.route("/api/games/<int:game_id>/play/move/", methods=["POST"])
@token_required
def player_move(game_id):

    if None in ([request.form.get("x"), request.form.get("y")]):
        return api_error("Some of the required parameters x and y are missing", 004), 400

    try:
        req = MoveRequest(
            x=request.form.get("x", None, type=int),
            y=request.form.get("y", None, type=int),
            gameId=game_id,
            userId=g.user.id
        )

        rep = gameservice.send(req, timeout=5000)
        if isinstance(rep, GameError):
            return api_error(rep.description, rep.code)
        else:
            return "" # assuming this returns 200 OK
    except TimeoutError as e:
        return api_error("Game service not available", 500), 500
    except Exception as e:
        return api_error("Service not available", 500), 500

@app.route("/api/games/<int:game_id>/play/question/", methods=["POST"])
@token_required
def question(game_id):
    try:
        req = QuestionRequest(
            gameId=game_id,
            userId=g.user.id
        )

        rep = gameservice.send(req)
        if isinstance(rep, GameError):
            return api_error(rep.description, rep.code)
        else:
            return jsonify({ "question" : rep.question, "alternatives" : [a for a in rep.alternatives] })
    except TimeoutError as e:
        return api_error("Game service not available", 500)
    except Exception as e:
        traceback.print_exc(sys.stdout)
        return api_error("Service not available", 500), 500

@app.route("/api/games/<int:game_id>/play/answer/", methods=["POST"])
@token_required
def answer(game_id):
    try:
        answer = request.form.get("answer", type=int)
        if not answer:
            return api_error("Missing required parameter answer", 400), 400

        req = AnswerRequest(
            gameId=game_id,
            userId=g.user.id,
            answer=answer
        )

        rep = gameservice.send(req)
        if isinstance(rep, GameError):
            return api_error(rep.description, rep.code)
        else:
            return jsonify({ "isCorrect" : rep.isCorrect })
    except TimeoutError as e:
        return api_error("Game service not available", 500)
    except Exception as e:
        return api_error("Service not available", 500), 500


@app.route("/api/games/<int:game_id>/events/")
def game_listener(game_id):
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']

        sock = zmq_ctx.socket(zmq.SUB)
        sock.connect("tcp://*:5202")
        sock.setsockopt(zmq.SUBSCRIBE, "game-%d" % game_id)

        while True:
            print "started websocket listener"
            game_id, msg_type, msg = sock.recv_multipart()
            cls = protocol_mapper.get(int(msg_type))
            message = cls.FromString(msg)
            print "deseralized type: %s" % message.__class__.__name__

            if isinstance(message, BoardChangePubSubMessage):
                ws.send(json.dumps({"type": "board_change", "payload": {"board": list(message.game.board)}}))
            elif isinstance(message, NewRoundPubSubMessage):
                ws.send(json.dumps({"type": "new_round", "payload": {}}))
            else:
                ws.send(json.dumps({"type": "unknown", "payload": {"msg_type": msg_type}})) # only used to debug
    abort(404) # only accessible from websockets
