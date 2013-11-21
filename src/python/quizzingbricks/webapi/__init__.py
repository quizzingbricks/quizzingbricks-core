# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

from itsdangerous import URLSafeTimedSerializer
from functools import wraps
from flask import Flask, jsonify, request, g

from quizzingbricks.client.exceptions import TimeoutError
from quizzingbricks.client.users import UserServiceClient
from quizzingbricks.common.protocol import GetUserRequest, GetUserResponse

app = Flask(__name__)
app.secret_key = "dev-key-123"

token_signer = URLSafeTimedSerializer("dev-key-abc123")

userservice = UserServiceClient("tcp://*:5551")

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

@app.route("/")
def api_index():
    return jsonify({
        "api": "Quizzing Bricks",
        "endpoints": map(lambda x: {"endpoint": x.rule, "method": list(x.methods)}, app.url_map.iter_rules())
    })

from quizzingbricks.webapi import users, games, friends
