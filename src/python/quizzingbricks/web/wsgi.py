# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

from quizzingbricks.web import app
from werkzeug.debug import DebuggedApplication

app.debug = True
app = DebuggedApplication(app)