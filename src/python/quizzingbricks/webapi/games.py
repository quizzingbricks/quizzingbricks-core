# -*- coding: utf-8 -*-
"""
    Copyright (C) Quizzingbricks
"""
from flask import request, jsonify, g

from quizzingbricks.webapi import app, api_error, api_errors, token_required
from quizzingbricks.client.games import GameServiceClient
from quizzingbricks.client.exceptions import TimeoutError

gameservice = GameServiceClient("tcp://*:1234")

@app.route("/api/game/<int:gameid>", methods=["POST"])
def request_info(gameid):
    msg = GameInfoRequest()
    msg.gameId = gameid


    try:
        rep = gameservice.send(msg)
        if isinstance(rep, GameError):
            return api_error(rep.description, rep.code)
        else:
            return jsonify({ "gameId" : rep.gameId,
                             "players" : [ { "userId" : player.userId,
                                            "state" : player.state,
                                            "x" : player.x,
                                            "y" : player.y,
                                            "question" : player.question,
                                            "alternatives" : [a for a in player.alternatives],
                                            "answeredCorrectly" : player.answeredCorrectly } for player in rep.players ],
                             "board" : [ b for b in rep.board ]
                          })
    except TimeoutError as e:
        return api_error("Game service not available", 500)

@app.route("/api/game/<int:gameid>/play/move", methods=["POST"])
def player_move(gameid):
    msg = PlayerMove()
    msg.x = request.form.get("x", None) # I have no idea if this is the correct way of getting this info
    msg.y = request.form.get("y", None)
    msg.gameId = gameid
    msg.userId = g.user.id # I have no idea if this is the correct way of getting this info

    try:
        rep = gameservice.send(msg)
        if isinstance(rep, GameError):
            return api_error(rep.description, rep.code)
        else:
            return "" # assuming this returns 200 OK
    except TimeoutError as e:
        return api_error("Game service not available", 500)

@app.route("/api/game/<int:gameid>/play/question", methods=["POST"])
def question(gameid):
    msg = QuestionRequest()
    msg.gameId = gameid
    msg.userId = g.user.id

    try:
        rep = gameservice.send(msg)
        if isinstance(rep, GameError):
            return api_error(rep.description, rep.code)
        else:
            return jsonify({ "question" : rep.question, "alternatives" : [a for a in rep.alternatives] })
    except TimeoutError as e:
        return api_error("Game service not available", 500)

@app.route("/api/game/<g_id>/play/answer")
def answer(gameid):
    msg = AnswerRequest()
    msg.gameId = gameId
    msg.userId = g.user.id
    msg.answer = request.form.get("answer", None)

    try:
        rep = gameservice.send(msg)
        if isinstance(rep, GameError):
            return api_error(rep.description, rep.code)
        else:
            return jsonify({ "isCorrect" : rep.isCorrect })
    except TimeoutError as e:
        return api_error("Game service not available", 500)