# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

from quizzingbricks.client.users import UserServiceClient
from quizzingbricks.common.protocol import LoginRequest

def main():
    uc = UserServiceClient("tcp://*:5551")

    lr = LoginRequest()
    lr.email = "demo@qb.se"
    lr.password = "demo"
    response = uc.authenticate(lr, timeout=5000) # timeout on 5 seconds
    print response.__class__.__name__

    lr2 = LoginRequest()
    lr2.email = "fail@fail.se"
    lr2.password = "fail"
    response2 = uc.authenticate(lr2, timeout=5000)
    print response2.__class__.__name__

if __name__ == "__main__":
    main()
