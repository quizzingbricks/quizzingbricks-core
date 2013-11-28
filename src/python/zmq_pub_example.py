# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

import gevent
import zmq.green as zmq

def main():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUB)
    sock.connect("tcp://*:5201")

    while True:
        gevent.sleep(10)
        sock.send_multipart(["1", "hello"])
        print "publisher sent!"

if __name__ == "__main__":
    main()