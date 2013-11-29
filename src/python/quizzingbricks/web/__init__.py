from flask import Flask
from werkzeug.debug import DebuggedApplication
import zmq.green as zmq


from quizzingbricks.client.users import UserServiceClient
from quizzingbricks.client.lobby import LobbyServiceClient
from quizzingbricks.client.friends import FriendServiceClient
from quizzingbricks.client.games import GameServiceClient



zmq_ctx = zmq.Context(1)

userservice = UserServiceClient("tcp://*:5551", zmq_context=zmq_ctx)
lobbyservice = LobbyServiceClient("tcp://*:5552", zmq_context=zmq_ctx)
friendservice = FriendServiceClient("tcp://*:5553", zmq_context=zmq_ctx)
gameservice = GameServiceClient("tcp://*:1234", zmq_context=zmq_ctx)

SECRET_KEY = 'development key'
app = Flask(__name__)
app.config.from_object(__name__)

import quizzingbricks.web.views