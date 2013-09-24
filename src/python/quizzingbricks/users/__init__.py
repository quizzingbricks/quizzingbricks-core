# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

from quizzingbricks.nuncius import NunciusService, expose

class UserService(NunciusService):
    name = "userservice"

    @expose("authenticate")
    def authenticate_by_password(request):
        pass

    @expose("authenticate_by_token")
    def authenticate_by_token(request):
        pass