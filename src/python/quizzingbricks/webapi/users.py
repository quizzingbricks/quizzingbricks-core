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
    RegistrationResponse, GetUserRequest, GetUserResponse,
    RpcError)

userservice = UserServiceClient("tcp://*:5551")

@app.route("/api/users/login/", methods=["POST"])
def login():
    email = request.form.get("email", None)
    password = request.form.get("password", None)

    if None in (email, password):
        return api_error("E-mail or password is missing, check your data", 1), 400 # TODO: define a error code list

    login_req = LoginRequest(email=email, password=password)

    try:
        response = userservice.authenticate(login_req, timeout=3000) # timeout after 3 seconds

        #handle response.userId
        if isinstance(response, LoginResponse):
            return jsonify({"token": token_signer.dumps(response.userId)})
        if isinstance(response, RpcError):
            errors = {
                1: {"message": "Internal service error", "code": "000"},
                5: {"message": "Wrong email or password", "code": "010"},
            }

            return api_error(**errors.get(response.error_code, {"message": "Error code not defined"})), 400
        #return api_error("Wrong password", 501)
    except TimeoutError as e:
        return api_error("Service not available", 500) # ???

@app.route("/api/users/", methods=["POST"]) # change to post
def create_user():
    email = request.form.get("email")
    password = request.form.get("password")

    if not (password or email):
        return api_error("Missing email or password", 102), 400

    try:
        response = userservice.create_user(RegistrationRequest(email=email, password=password), timeout=5000) # timeout after 5 sec

        if isinstance(response, RegistrationResponse):
            return str(response.userId)
        elif isinstance(response, RpcError):
            errors = {
                1: {"message": "Internal service error", "code": "000"},
                11: {"message": "This mail is already taken", "code": "101"},
            }

            return api_error(**errors.get(response.error_code, {"message": "Error code not defined"})), 400
    except TimeoutError as e:
        return api_error("Service not available", 500)


@app.route("/api/users/me/")
@token_required
def get_current_user():
    return jsonify({
        "id": g.user.id,
        "email": g.user.email
    })
