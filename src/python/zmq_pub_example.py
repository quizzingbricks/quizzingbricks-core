# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

import gevent
import json
import random
import zmq.green as zmq
from quizzingbricks.common.protocol import BoardChangePubSubMessage, Game, protocol_inverse_mapper


def main():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUB)
    sock.connect("tcp://*:5201")

    while True:
        game = Game(
            gameId = 1,
            board = [random.choice([1,2,0,0,0]) for x in xrange(64)]
        )

        req = BoardChangePubSubMessage(game=game)

        sock.send_multipart([
            "game-1",
            str(protocol_inverse_mapper[req.__class__.__name__]),
            req.SerializeToString()
        ])
        print "publisher sent!"
        gevent.sleep(10)

if __name__ == "__main__":
    main()