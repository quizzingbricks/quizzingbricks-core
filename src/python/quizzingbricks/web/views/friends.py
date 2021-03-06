

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify

import sys, traceback

from collections import namedtuple
from quizzingbricks.web import app, friendservice
from quizzingbricks.web.views.utils import get_friends_list


from quizzingbricks.client.friends import FriendServiceClient
from quizzingbricks.common.protocol import (
    AddFriendRequest, AddFriendResponse, RemoveFriendRequest, RemoveFriendResponse
    )

#friendservice = FriendServiceClient("tcp://*:5553")
from quizzingbricks.web import login_required


@app.route('/add_friend', methods=['GET', 'POST'])
@login_required
def add_friend():
    if request.method == 'POST':
        friend_Email = request.form['friend_email']
        if(friend_Email!= ""):
            add_friend_response = friendservice.add_friend(AddFriendRequest(userId=session['userId'],friend_email=friend_Email))
            if (isinstance(add_friend_response, AddFriendResponse)):
                #print "add response", add_friend_response
                #friends_list = get_friends_list()
                return redirect(url_for('friends'))
        else:
            #friends_list = get_friends_list()
            return redirect(url_for('friends_list', msg="Must fill in email of user you want to add"))   
    else:
        #friends_list = get_friends_list()
        return redirect(url_for('friends'))    

@app.route('/remove_friend', methods=['GET', 'POST'])
@login_required
def remove_friend():

    if request.method == 'POST':    # removes selected friend and fetches the rest of the friendslist again if more is to be removed
        try:
            print "before call"

            try:
                print "friendId", int(request.form['friend'])
                remove_friend_response = friendservice.remove_friend(RemoveFriendRequest(userId =session['userId'],friendId=int(request.form['friend'])))
            except:
                print "Exception in user code:"
                print '-'*60
                traceback.print_exc(file=sys.stdout)
                print '-'*60



            #remove_friend_response = friendservice.remove_friend(RemoveFriendRequest(userId =session['userId'],friendId=int(request.form['friend'])))
            print "remove response", remove_friend_response
            if (isinstance(remove_friend_response, RemoveFriendResponse)):
                
                print "remove response", remove_friend_response
                
                return redirect(url_for('friends_list', msg ="User removed from friends list"))
        except: #no radio buttons selected
            #friends_list = get_friends_list()
            return redirect(url_for('friends_list', msg="Must select radio button"))
    else:
        #friends_list = get_friends_list()
        return redirect(url_for('friends'))




@app.route('/friends_list/<msg>' )
@login_required
def friends_list(msg):
    print msg
    return render_template('friends_list.html', friends_list=get_friends_list(),
                                                    error=msg)

@app.route('/friends_list')
@login_required
def friends():
    return render_template('friends_list.html', friends_list=get_friends_list())




            #     try:
            #     remove_friend_response = friendservice.remove_friend(RemoveFriendRequest(userId =session['userId'],friendId=int(request.form['friend'])))
            # except:
            #     print "Exception in user code:"
            #     print '-'*60
            #     traceback.print_exc(file=sys.stdout)
            #     print '-'*60