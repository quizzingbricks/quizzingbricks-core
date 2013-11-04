# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

from flask import Flask, jsonify, request, g

from quizzingbricks.client.exceptions import TimeoutError
from quizzingbricks.client.users import UserServiceClient
from quizzingbricks.common.protocol import (
    LoginRequest, LoginResponse, RegistrationRequest, RegistrationResponse
)

app = Flask(__name__)
app.secret_key = "dev-key-123"

userservice = UserServiceClient("tcp://*:5551")
#gameservice = GameServiceClient("tcp://*:xxxx")

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
    g.user_id = None

from quizzingbricks.services.users.models import User
from quizzingbricks.common.db import session

@app.route("/api/users/login/", methods=["GET"])
def login():
    username = "demo@demo.se"#request.form.get("username", None)
    password = "demo.2"#request.form.get("password", None)

    if None in (username, password):
        return api_error("Username or password is missing, check your data", 1) # TODO: define a error code list

    login_req = LoginRequest()
    login_req.email = "demo@qb.se"
    login_req.password = "demo"

    try:
        #response = userservice.authenticate(login_req) # timeout after 3 seconds

        #handle response.userId
        #if isinstance(response, LoginResponse):
        #    return "token#%s" % response.userId # TODO: just a temporary thing, implement something real...
        #return api_error(response.message) # TODO: check that the response is a RpcError
        user = User.query.filter(User.email==login_req.email).first()
        session.close()
        if user and user.check_password(login_req.password):
            return "_token#%s" % user.id
        return api_error("Wrong password", 501)
    except TimeoutError as e:
        return api_error("Service not available", 500) # ???

@app.route("/api/users/", methods=["GET"]) # change to post
def create_user():
    email = "hello@hello.se"
    password = "something"

    req = RegistrationRequest()
    req.email = email
    req.password = password

    rep = userservice.create_user(req)

    return rep.userId

@app.route("/api/game/<int:gameid>/play/move", methods=["POST"])
def place_brick(gameid):
    return "tbd"