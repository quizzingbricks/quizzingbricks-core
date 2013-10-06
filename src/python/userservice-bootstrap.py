# -*- coding: utf-8 -*-
"""
    Copyright (C) Quizzing Bricks
"""

from quizzingbricks.users import UserService

if __name__ == "__main__":
    print "UserService started"
    print "-" * 19
    print "Ctrl^C to interrupt"
    service = UserService("tcp://*:5551")
    service.run()
