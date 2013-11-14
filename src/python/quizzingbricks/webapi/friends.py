# -*- coding: utf-8 -*-
"""
    Copyright (C) Quizzingbricks
"""

from flask import request, jsonify, g

from quizzingbricks.webapi import app, api_error, api_errors, token_required, token_signer
from quizzingbricks.client.friends import FriendServiceClient
from quizzingbricks.client.exceptions import TimeoutError
from quizzingbricks.common.protocol import (
    AddFriendRequest, GetFriendsRequest
)
import traceback

friendservice = FriendServiceClient("tcp://*:5553")

@app.route("/api/users/me/friends/", methods=["GET"])
@token_required
def get_friends():
    try:
        friends = friendservice.get_friends(GetFriendsRequest(userId=g.user.id))

        return jsonify({"friends": list(friends.friends_list)})
    except Exception as e:
        print "friends:", e
        traceback.print_exc()
        return api_error("Service not available", 500), 500


@app.route("/api/users/me/friends", methods=["POST"])
@token_required
def add_friend():
    pass