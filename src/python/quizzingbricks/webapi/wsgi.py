# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

from quizzingbricks.webapi import app
from werkzeug.debug import DebuggedApplication

class WebSocketDebuggedApplication(DebuggedApplication):
    """http://stackoverflow.com/a/18552263"""
    def __call__(self, environ, start_response):
        # check if websocket call
        if "wsgi.websocket" in environ and not environ["wsgi.websocket"] is None:
            # a websocket call, no debugger ;)
            return self.app(environ, start_response)
        # else go on with debugger
        return DebuggedApplication.__call__(self, environ, start_response)

app.debug = True
app = WebSocketDebuggedApplication(app)