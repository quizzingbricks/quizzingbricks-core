# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

from quizzingbricks.webapi import app
from werkzeug.debug import DebuggedApplication

app.debug = True
app = DebuggedApplication(app)