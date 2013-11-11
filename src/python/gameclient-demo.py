
# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

from quizzingbricks.client.games import GameServiceClient
from quizzingbricks.common.protocol import *
from quizzingbricks.client.exceptions import TimeoutError
from flask import jsonify
import json

from flask import Flask
app = Flask(__name__)

@app.route('/')
def main():
    gameservice = GameServiceClient("tcp://*:1234")
    msg = GameInfoRequest()
    msg.gameId = 1
    sideLength = 8

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

if __name__ == '__main__':
    app.run(host='0.0.0.0')