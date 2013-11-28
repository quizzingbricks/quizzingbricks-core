from flask import Flask
from werkzeug.debug import DebuggedApplication


from quizzingbricks.client.users import UserServiceClient
from quizzingbricks.client.lobby import LobbyServiceClient
from quizzingbricks.client.friends import FriendServiceClient
from quizzingbricks.client.games import GameServiceClient


userservice = UserServiceClient("tcp://*:5551")
lobbyservice = LobbyServiceClient("tcp://*:5552")
friendservice = FriendServiceClient("tcp://*:5553")
gameservice = GameServiceClient("tcp://*:1234")


SECRET_KEY = 'development key'
app = Flask(__name__)
app.config.from_object(__name__)

import quizzingbricks.web.views