# -*- coding: utf-8 -*-
"""
    Copyright (C) Quizzing Bricks
"""

from quizzingbricks.services.lobby import LobbyService

if __name__ == "__main__":
    print "LobbyService started"
    print "-" * 19
    print "Ctrl^C to interrupt"
    service = LobbyService("tcp://*:5552")
    service.run()
