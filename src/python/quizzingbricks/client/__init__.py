# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""
from contextlib import contextmanager
import json

import zmq.green as zmq
from quizzingbricks.common.protocol import *
from quizzingbricks.common.protocol import protocol_inverse_mapper, protocol_mapper
from quizzingbricks.client.exceptions import TimeoutError

class BaseClient(object):
    def __init__(self, uri, zmq_context=None):
        self.uri = uri
        self.zmq_ctx = zmq_context or zmq.Context()

    @contextmanager
    def rpc_call(self, method, request, timeout):
        """Handle the packaging for the transport which means
        that
        """
        socket = self.zmq_ctx.socket(zmq.REQ)
        socket.connect(self.uri)
        try:
            socket.send(json.dumps([method, protocol_inverse_mapper[request.__class__.__name__]]), zmq.SNDMORE)
            socket.send(request.SerializeToString())

            if timeout:
                poller = zmq.Poller()
                poller.register(socket, zmq.POLLIN)

                if poller.poll(timeout):
                    response_type = socket.recv()
                    response = socket.recv()
                else:
                    raise TimeoutError("Timeout error during RPC call")
            else:
                response_type = socket.recv()
                response = socket.recv()

            message = protocol_mapper[int(response_type)]()
            message.ParseFromString(response)

            yield message
        finally:
            socket.close()
