# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

from itsdangerous import URLSafeTimedSerializer
from functools import wraps
from flask import Flask, jsonify, request, g

from quizzingbricks.client.exceptions import TimeoutError
from quizzingbricks.client.games import GameServiceClient
from quizzingbricks.client.users import UserServiceClient
from quizzingbricks.common.protocol import (
    LoginRequest, LoginResponse, RegistrationRequest, RegistrationResponse, GetUserRequest, GetUserResponse,
    CreateGame, GameInfoRequest, GameInfoResponse, PlayerMove, GameError
)

app = Flask(__name__)
app.secret_key = "dev-key-123"

token_signer = URLSafeTimedSerializer("dev-key-abc123")

userservice = UserServiceClient("tcp://*:5551")
gameservice = GameServiceClient("tcp://*:1234")

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if hasattr(g, "user") and g.user is None:
            return api_error("Invalid or missing token", 100)
        return f(*args, **kwargs)
    return decorated_function

def api_error(message, code=0):
    """Returns a single error message"""
    # TODO: rewrite to internal use the api_errors or keep this?
    return jsonify(
        {"errors": [
            {"message": message, "code": code}
        ]}
    )

def api_errors(message_code_pairs):
    """Return multiple error messages"""
    return jsonify(
        {"errors": [ {"message": msg, "code": code} for msg, code in message_code_pairs ]}
    )

@app.before_request
def set_current_user():
    # TODO: implement to check the auth token header or querystring
    #g.user_id = -1
    user_token = request.args.get("token") or request.headers.get("token")
    if user_token:
        try:
            user_id = token_signer.loads(user_token, max_age=6048000) # 7 days
            user_rep = userservice.get_user(GetUserRequest(userId=user_id))
            if isinstance(user_rep, GetUserResponse):
                g.user = user_rep.user
            else:
                g.user = None
        except:
            g.user = None
    else:
        g.user = None

from quizzingbricks.services.users.models import User
from quizzingbricks.common.db import session

@app.route("/api/users/login/", methods=["POST"])
def login():
    email = request.form.get("email", None)
    password = request.form.get("password", None)

    if None in (email, password):
        return api_error("E-mail or password is missing, check your data", 1) # TODO: define a error code list

    login_req = LoginRequest(email=email, password=password)

    try:
        response = userservice.authenticate(login_req, timeout=3000) # timeout after 3 seconds

        #handle response.userId
        if isinstance(response, LoginResponse):
            return jsonify({"token": token_signer.dumps(response.userId)})
        return api_error(response.message) # TODO: check that the response is a RpcError
        #return api_error("Wrong password", 501)
    except TimeoutError as e:
        return api_error("Service not available", 500) # ???

@app.route("/api/users/", methods=["POST"]) # change to post
def create_user():
    email = "hello@hello.se"
    password = "something"

    req = RegistrationRequest()
    req.email = email
    req.password = password

    rep = userservice.create_user(req)

    return rep.userId

@app.route("/api/users/me/")
@token_required
def get_current_user():
    return jsonify({
        "id": g.user.id,
        "email": g.user.email
    })

@app.route("/api/game/<int:gameid>", methods=["POST"])
def request_info(gameid):
    msg = GameInfoRequest()
    msg.gameId = gameid


    try:
        rep = gameservice.send(msg)
        if isinstance(rep, GameError):
            return api_error(rep.description, rep.code)
        else:
            return jsonify({ "gameId" : rep.gameId,
                             "players" : [ { "userId" : player.userId, 
                                            "state" : player.state,
                                            "x" : player.x,
                                            "y" : player.y,
                                            "question" : player.question,
                                            "alternatives" : [a for a in player.alternatives],
                                            "answeredCorrectly" : player.answeredCorrectly } for player in rep.players ],
                             "board" : [ b for b in rep.board ]
                          })
    except TimeoutError as e:
        return api_error("Game service not available", 500)

@app.route("/api/game/<int:gameid>/play/move", methods=["POST"])
def player_move(gameid):
    msg = PlayerMove()
    msg.x = request.form.get("x", None) # I have no idea if this is the correct way of getting this info
    msg.y = request.form.get("y", None)
    msg.gameId = gameid
    msg.userId = g.user.id # I have no idea if this is the correct way of getting this info

    try:
        rep = gameservice.send(msg)
        if isinstance(rep, GameError):
            return api_error(rep.description, rep.code)
        else:
            return "" # assuming this returns 200 OK
    except TimeoutError as e:
        return api_error("Game service not available", 500)

@app.route("/api/game/<int:gameid>/play/question", methods=["POST"])
def question(gameid):
    msg = QuestionRequest()
    msg.gameId = gameid
    msg.userId = g.user.id

    try:
        rep = gameservice.send(msg)
        if isinstance(rep, GameError):
            return api_error(rep.description, rep.code)
        else:
            return jsonify({ "question" : rep.question, "alternatives" : [a for a in rep.alternatives] })
    except TimeoutError as e:
        return api_error("Game service not available", 500)

@app.route("/api/game/<g_id>/play/answer")
def answer(gameid):
    msg = AnswerRequest()
    msg.gameId = gameId
    msg.userId = g.user.id
    msg.answer = request.form.get("answer", None)

    try:
        rep = gameservice.send(msg)
        if isinstance(rep, GameError):
            return api_error(rep.description, rep.code)
        else:
            return jsonify({ "isCorrect" : rep.isCorrect })
    except TimeoutError as e:
        return api_error("Game service not available", 500)