# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

from gevent.wsgi import WSGIServer
from quizzingbricks.webapi import app

if __name__ == "__main__":
    http_server = WSGIServer(('', 8100), app)
    http_server.serve_forever()
    #app.run(host="0.0.0.0", debug=True)