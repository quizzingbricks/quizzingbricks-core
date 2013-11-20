# -*- coding: utf-8 -*-
"""
    Copyright (C) Quizzingbricks
"""

from flask import request, jsonify, g

from quizzingbricks.webapi import app, api_error, api_errors, token_required, token_signer
from quizzingbricks.client.friends import FriendServiceClient
from quizzingbricks.client.exceptions import TimeoutError
from quizzingbricks.common.protocol import (
    AddFriendRequest, GetFriendsRequest,
    AddFriendResponse, RemoveFriendRequest, RemoveFriendResponse)
import traceback

friendservice = FriendServiceClient("tcp://*:5553")

@app.route("/api/users/me/friends/", methods=["GET"])
@token_required
def get_friends():
    try:
        response = friendservice.get_friends(GetFriendsRequest(userId=g.user.id))

        return jsonify({"friends": map(
            lambda user: dict(id=user.id, email=user.email),
            response.friends
        )})
    except Exception as e:
        print "friends:", e
        traceback.print_exc()
        return api_error("Service not available", 500), 500


@app.route("/api/users/me/friends/", methods=["POST"])
@token_required
def add_friend():
    try:
        email = request.form.get("friend")
        if not email:
            # or a error message that tells that the email is missing?
            return api_error("Missing required friend parameter", 004), 400

        response = friendservice.add_friend(AddFriendRequest(userId=g.user.id,friend_email=email))
        if isinstance(response, AddFriendResponse):
            if response.friend_added:
                return "OK"
            return api_error("No such user exists"), 400
        else:
            return api_error("Internal service error", 000), 400

    except Exception as e:
        print "add_friend", e
        traceback.print_exc()
        return api_error("Service not available", 500), 500

@app.route("/api/users/me/friends/", methods=["DELETE"])
@token_required
def delete_friend():
    try:
        friend_email = request.args.get("friend")
        if not friend_email:
            return api_error("Missing required friend parameter", 004), 400

        response = friendservice.remove_friend(RemoveFriendRequest(userId=g.user.id, friend_email=friend_email), timeout=5000)
        if not isinstance(response, RemoveFriendResponse):
            return api_error("Internal service error", 500), 500 # probably return RpcError
        return "OK" if response.friend_removed else (api_error("No such user exists", "011"), 200)
    except Exception as e:
        print "DELETE_FRIEND-ERROR:", e
        traceback.print_exc()
        return api_error("Service not available", 500), 500