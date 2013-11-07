# -*- coding: utf-8 -*-
"""
    Copyright (C) Quizzing Bricks
"""

from quizzingbricks.services.friends import FriendService

if __name__ == "__main__":
    print "FriendService started"
    print "-" * 19
    print "Ctrl^C to interrupt"
    service = FriendService("tcp://*:5553")
    service.run()