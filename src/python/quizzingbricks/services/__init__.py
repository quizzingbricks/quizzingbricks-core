# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks

    Internal protocol error codes
    =============================
    Global                  1: Wrong message type
                            2: Object does not exists

    UserService
    -----------
    * authenticate          5: Wrong email or password

    * create_user           10: Email or password is not present
                            11: Email is already taken

    FriendService
    -------------
    * ...

    LobbyService
    ------------
    * anwer_lobby_invite    30: Not permitted to the lobby
                            31: Lobby is full

    * start_game            35: No permission to manage the lobby

"""