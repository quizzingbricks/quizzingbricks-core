# -*- coding: utf-8 -*-
"""
    Copyright (C) Quizzingbricks
"""

from flask import request, jsonify

from quizzingbricks.webapi import app, api_error, api_errors, token_required, token_signer
from quizzingbricks.client.friends import FriendServiceClient
from quizzingbricks.client.exceptions import TimeoutError
from quizzingbricks.common.protocol import (
    AddFriendRequest,
)

friendservice = FriendServiceClient("tcp://*:5552")