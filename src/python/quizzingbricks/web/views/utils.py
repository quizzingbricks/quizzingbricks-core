

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify

import sys, traceback

from collections import namedtuple
from quizzingbricks.web import app, friendservice




from quizzingbricks.common.protocol import (
    GetFriendsRequest, GetFriendsResponse
    )





def get_friends_list():
    friends_list=[]
    Friend = namedtuple("Friend", ("id", "email"))
    friends_response = friendservice.get_friends(GetFriendsRequest(userId=session['userId']), timeout=5000)  #hard coded userId
    if (isinstance(friends_response,GetFriendsResponse)):
        for friend in friends_response.friends:
            friends_list.append(Friend(friend.id, friend.email))
    return friends_list