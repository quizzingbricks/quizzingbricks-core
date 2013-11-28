#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import argparse
import sys
import os
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


class QuizzingBricksCLI(object):
    def _run_web(self, port):
        # https://coderwall.com/p/q2mrbw
        port = port or 5000

        print "starting web server on", port
        from quizzingbricks.web import app
        from gevent.wsgi import WSGIServer

        app.debug =True

        http_server = WSGIServer(('', port), DebuggedApplication(app))
        http_server.serve_forever()

    def _run_webapi(self, port):
        from geventwebsocket.handler import WebSocketHandler

        port = port or 8100
        print "starting web-api server on", port
        from gevent.pywsgi import WSGIServer
        from quizzingbricks.webapi import app
        from flask import request
        import json
        import zmq.green as zmq

        # TODO: this is just temporary
        #   to experiment with websockets, will be moved into games.py later

        # https://gist.github.com/abhinavsingh/6378134
        # https://github.com/heroku-examples/python-websockets-chat/blob/master/chat.py
        # https://gist.github.com/lrvick/1185629
        # http://toastdriven.com/blog/2011/jul/31/gevent-long-polling-you/

        @app.route("/ws/<int:game_id>/")
        def test_ws(game_id):
            if request.environ.get('wsgi.websocket'):
                print "welcome to the websocket!"
                ws = request.environ['wsgi.websocket']
                if game_id == 5: # just testing
                    ws.close()
                    return
                ctx = zmq.Context(1)
                sock = ctx.socket(zmq.SUB)
                sock.connect("tcp://*:5202")
                sock.setsockopt(zmq.SUBSCRIBE, "game-1")#"game-%d" % game_id)
                while True:
                    #message = ws.receive()
                    #ws.send(json.dumps({"game_id": game_id, "data": message}))
                    message = sock.recv_json()
                    ws.send(json.dumps({"game_id": game_id, "data": message}))
            return "URL only allowed to access via websocket connection",400
        app.debug = True

        http_server = WSGIServer(('', port), WebSocketDebuggedApplication(app, evalex=True), handler_class=WebSocketHandler)
        http_server.serve_forever()

    def _run_userservice(self, port):
        from quizzingbricks.services.users import UserService

        port = port or 5551
        msg = "UserService started on port", port
        print msg
        print "-" * len(msg)
        print "Ctrl^C to interrupt"
        service = UserService("tcp://*:%d" % port)
        service.run()

    def _run_lobbyservice(self, port):
        from quizzingbricks.services.lobby import LobbyService

        port = port or 5552
        msg = "LobbyService started on port", port
        print msg
        print "-" * len(msg)
        print "Ctrl^C to interrupt"
        service = LobbyService("tcp://*:%d" % port)
        service.run()

    def _run_friendservice(self, port):
        from quizzingbricks.services.friends import FriendService

        port = port or 5553
        msg = "FriendService started on port", port
        print msg
        print "-" * len(msg)
        print "Ctrl^C to interrupt"
        service = FriendService("tcp://*:%d" % port)
        service.run()


    def _run_zmq_pubsub_forwarder(self, frontend_port, backend_port):
        import zmq.green as zmq

        ctx = zmq.Context()

        frontend_port = frontend_port or 5201
        backend_port = backend_port or 5202

        print "Starting ZeroMQ forwarder (pubsub)"
        print "frontend (publisher):", frontend_port
        print "backend (consumers):", backend_port

        frontend = ctx.socket(zmq.SUB)
        frontend.bind("tcp://*:%s" % frontend_port)
        frontend.setsockopt(zmq.SUBSCRIBE, "")

        backend = ctx.socket(zmq.PUB)
        backend.bind("tcp://*:%s" % backend_port)

        zmq.device(zmq.FORWARDER, frontend, backend)

    def run(self):
        parser = argparse.ArgumentParser("quizctl", description="CLI for Quizzingbricks")
        subparsers = parser.add_subparsers(help="sub command...", dest="command")

        run_web_parser = subparsers.add_parser("web", help="Start the web server")
        run_web_parser.add_argument("-port", type=int, help="Port to use for the web server (default is 5000)")

        run_webapi_parser = subparsers.add_parser("webapi", help="Start the web-api server")
        run_webapi_parser.add_argument("-port", type=int, help="Port to use for the web-api server (default is 8100)")

        run_userservice_parser = subparsers.add_parser("userservice", help="Start the user service (server)")
        run_userservice_parser.add_argument("-port", type=int, help="Port to use for the userservice (default is 5551")

        run_lobbyservice_parser = subparsers.add_parser("lobbyservice", help="Start the lobby service (server)")
        run_lobbyservice_parser.add_argument("-port", type=int, help="Port to use for the lobby service (default is 5552)")

        run_friendservice_parser = subparsers.add_parser("friendservice", help="Start the friend service (server)")
        run_friendservice_parser.add_argument("-port", type=int, help="Port to use for the lobby service (default is 5553)")

        run_zmq_pubsub_parser = subparsers.add_parser("pubsub", help="Start a ZeroMQ forwarder (aka broker?)")
        run_zmq_pubsub_parser.add_argument("-frontend", type=int, help="Port to use for the publisher(s)")
        run_zmq_pubsub_parser.add_argument("-backend", type=int, help="Port to use for the consumer(s)")

        args = parser.parse_args()

        if args.command == "web":
            self._run_web(args.port)
        elif args.command == "webapi":
            self._run_webapi(args.port)
        elif args.command == "userservice":
            self._run_userservice(args.port)
        elif args.command == "lobbyservice":
            self._run_lobbyservice(args.port)
        elif args.command == "friendservice":
            self._run_friendservice(args.port)
        elif args.command == "pubsub":
            self._run_zmq_pubsub_forwarder(args.frontend, args.backend)


if __name__ == "__main__":
    QuizzingBricksCLI().run()