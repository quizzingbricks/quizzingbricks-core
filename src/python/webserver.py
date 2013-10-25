# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

from quizzingbricks.web.run_web import app
from gevent.wsgi import WSGIServer




if __name__ == "__main__":
	http_server = WSGIServer(('', 5000), app)
	http_server.serve_forever()
    #app.run(host="0.0.0.0", debug=True)