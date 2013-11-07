#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import argparse
import sys
import os

class QuizzingBricksCLI(object):
    def _run_web(self, port):
        port = port or 5000

        print "starting web server on", port
        from quizzingbricks.web.run_web import app
        from gevent.wsgi import WSGIServer

        http_server = WSGIServer(('', port), app)
        http_server.serve_forever()

    def _run_webapi(self, port):
        port = port or 8100
        print "starting web-api server on", port
        from gevent.wsgi import WSGIServer
        from quizzingbricks.webapi import app

        http_server = WSGIServer(('', port), app)
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

        args = parser.parse_args()

        if args.command == "web":
            self._run_web(args.port)
        elif args.command == "webapi":
            self._run_webapi(args.port)
        elif args.command == "userservice":
            self._run_userservice(args.port)
        elif args.command == "lobbyservice":
            self._run_lobbyservice(args.port)


if __name__ == "__main__":
    QuizzingBricksCLI().run()