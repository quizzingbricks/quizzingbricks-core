# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

from quizzingbricks.client.users import UserClient
from quizzingbricks.common.protocol import LoginRequest

def main():
    lr = LoginRequest()
    lr.email = "a"
    lr.password = "b"
    uc = UserClient("tcp://*:5551")
    response = uc.authenticate(lr, timeout=5000) # timeout on 5 seconds

    print response.__class__.__name__, response.userId

if __name__ == "__main__":
    main()
