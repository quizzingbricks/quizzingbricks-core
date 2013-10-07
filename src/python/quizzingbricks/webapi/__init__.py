# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

from flask import Flask, jsonify, request, g

from quizzingbricks.client.exceptions import TimeoutError
from quizzingbricks.client.users import UserServiceClient
from quizzingbricks.common.protocol import LoginRequest, LoginResponse

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


@app.route("/api/login/", methods=["POST"])
def login():
    username = request.form.get("username", None)
    password = request.form.get("password", None)

    if None in (username, password):
        return api_error("Username or password is missing, check your data", 1) # TODO: define a error code list

    login_req = LoginRequest()
    login_req.email = "demo@qb.se"
    login_req.password = "demo"

    try:
        response = userservice.authenticate(login_req, timeout=3000) # timeout after 3 seconds

        #handle response.userId
        if isinstance(response, LoginResponse):
            return "token#%s" % response.userId # TODO: just a temporary thing, implement something real...
        return api_error(response.message) # TODO: check that the response is a RpcError
    except TimeoutError as e:
        return api_error("Service not available", 500) # ???