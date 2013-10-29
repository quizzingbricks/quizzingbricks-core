
# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""
from quizzingbricks.client import BaseClient

class GameServiceClient(BaseClient):

    @contextmanager
    def rpc_call(self, request, timeout):
        """Handle the packaging for the transport which means
        that
        """
        socket = self.zmq_ctx.socket(zmq.REQ)
        socket.connect(self.uri)
        try:
            socket.send('%d' % (protocol_inverse_mapper[request.__class__.__name__]), zmq.SNDMORE)
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

    def create_game(self, request, timeout=None):
        with self.rpc_call(request, timeout) as response:
            return response

