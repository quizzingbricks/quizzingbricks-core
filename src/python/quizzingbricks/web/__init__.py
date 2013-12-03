from flask import Flask, url_for, redirect, session, g
from functools import wraps
from quizzingbricks.common.protocol import GetUserRequest
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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if hasattr(g, "user") and g.user is None:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def set_user():
    if "userId" in session:
        try:
            g.user = userservice.get_user(GetUserRequest(userId=session["userId"]))
        except:
            print "Exception in set_user (before_request)"
            g.user=None
    else:
        g.user = None

import quizzingbricks.web.views