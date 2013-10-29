
# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

from quizzingbricks.client.games import GameServiceClient
from quizzingbricks.common.protocol import CreateGame, GameInfoReply

def main():
    c = GameServiceClient("tcp://*:1234")

    cg = CreateGame()
    cg.players.append(1)
    cg.players.append(2)

    r = c.send(cg, timeout=5000)
    print r.__class__.__name__

if __name__ == "__main__":
    main()
