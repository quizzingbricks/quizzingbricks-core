# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

from quizzingbricks.webapi import app
from werkzeug.debug import DebuggedApplication

# TODO: use WebSocketDebuggedApplication (found in bin/quizctl.py)

app.debug = True
app = DebuggedApplication(app)