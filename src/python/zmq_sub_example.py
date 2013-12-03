# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

import gevent
import json
import random
import zmq.green as zmq
from quizzingbricks.common.protocol import *


def main():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.SUB)
    sock.bind("tcp://*:5201")
    sock.setsockopt(zmq.SUBSCRIBE, "game-1")

    while True:
        print "started websocket listener"
        game_id, msg_type, msg = sock.recv_multipart()
        cls = protocol_mapper.get(int(msg_type))
        message = cls.FromString(msg)
        print "deseralized type: %s" % message.__class__.__name__

        if isinstance(message, PlayerStateChangePubSubMessage):
            print(message.player.userId)
            print(message.player.state)
            print(message.player.score)
        elif isinstance(message, NewRoundPubSubMessage):
            print(message.game.gameId)
            print(message.game.players[0].state)
            print(message.game.board)
            #ws.send(json.dumps({"type": "new_round", "payload": {NewRoundPubSubMessage}}))
        #else:
          #  ws.send(json.dumps({"type": "unknown", "payload": {"msg_type": msg_type}})) # only used to debug

if __name__ == "__main__":
    main()
