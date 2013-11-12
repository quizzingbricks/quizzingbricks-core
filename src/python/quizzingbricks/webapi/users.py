# -*- coding: utf-8 -*-
"""
    Copyright (C) Quizzingbricks
"""

from flask import request, jsonify, g

from quizzingbricks.webapi import app, api_error, api_errors, token_required, token_signer
from quizzingbricks.client.users import UserServiceClient
from quizzingbricks.client.exceptions import TimeoutError
from quizzingbricks.common.protocol import (
    LoginRequest, LoginResponse, RegistrationRequest,
    RegistrationResponse, GetUserRequest, GetUserResponse
)

userservice = UserServiceClient("tcp://*:5551")

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
