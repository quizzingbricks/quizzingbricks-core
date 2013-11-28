
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify

import sys, traceback

from collections import namedtuple
from quizzingbricks.web import app, lobbyservice, gameservice
from quizzingbricks.web.views.utils import get_friends_list



from quizzingbricks.client.exceptions import TimeoutError
from quizzingbricks.common.protocol import (
    CreateLobbyRequest, CreateLobbyResponse, GetLobbyStateRequest, GetLobbyStateResponse, \
    AcceptLobbyInviteRequest, AcceptLobbyInviteResponse, InviteLobbyRequest, InviteLobbyResponse, \
    RemoveLobbyRequest, RemoveLobbyResponse, StartGameRequest, StartGameResponse,\
    GetLobbyListRequest, GetLobbyListResponse,CreateGameRequest, CreateGameResponse,\
    GameError
    )

@app.route('/lobby_invite/<int:game_type>/<int:lobby_id>',methods=['GET', 'POST'])
def lobby_invite(game_type,lobby_id):
    print "invite friends"
    print lobby_id
    print game_type
    friends = []
    friends_list = []  
    if request.method == 'POST':
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                if not value ==''  :
                    friends=friends+[value]
    lobby_invite_response = lobbyservice.inviteToLobby(InviteLobbyRequest(userId=session['userId'],lobbyId=lobby_id, invite_emails=friends))
    if (isinstance(lobby_invite_response, InviteLobbyResponse)):
        print lobby_invite_response
    friends_list = get_friends_list()
 
    
    return render_template('create_game.html' ,friends_list=friends_list, game_type=game_type, lobby_id=lobby_id)

@app.route('/lobby_state/<int:game_type>/<int:lobby_id>', methods=['GET', 'POST'])
def lobby_state(game_type, lobby_id):
    print "lobby state"  
    print game_type
    print lobby_id
    friends=[]
    accept_friends=[]
    deny_friends=[]
    none_friends=[]
    friends_list = []
    friends_list = get_friends_list()
    lobby_state_response = lobbyservice.getLobbyState(GetLobbyStateRequest(lobbyId=lobby_id))
    if (isinstance(lobby_state_response, GetLobbyStateResponse)):
        print lobby_state_response
        print len(lobby_state_response.users)
        #print lobby_state_response.friend_email[0]
        for x in range(0, len(lobby_state_response.users)):
            print lobby_state_response.users[x].email, lobby_state_response.answer[x]
            if (lobby_state_response.answer[x] == "Accept"):
                accept_friends = accept_friends + [lobby_state_response.users[x].email]
            if (lobby_state_response.answer[x] == "Deny"):
                deny_friends = deny_friends + [lobby_state_response.users[x].email]
            if (lobby_state_response.answer[x] == "None"):  
                none_friends = none_friends + [lobby_state_response.users[x].email]


    return render_template('create_game.html' ,none_friends = none_friends, deny_friends = deny_friends, accept_friends = accept_friends,friends=friends, friends_list=friends_list, game_type=game_type, lobby_id=lobby_id) 

@app.route('/lobby_list/<int:game_type>/<int:lobby_id>', methods=['GET', 'POST'])
def lobby_list(game_type, lobby_id):
    print "lobby list"  
    print game_type
    print lobby_id
    friends_list = []
    invited_lobbies = []
    friends_list = get_friends_list()
    print "innan response"
   
    lobby_list_response = lobbyservice.getLobbyList(GetLobbyListRequest(userId=session['userId']))
    #lobby_list_response = lobbyservice.getLobbyList(GetLobbyListRequest(userId=session['userId']))
    if (isinstance(lobby_list_response, GetLobbyListResponse)):

        #print lobby_list_response
        for x in range(0, len(lobby_list_response.lobbyIds)):
            print lobby_list_response.lobbyIds[x], lobby_list_response.status[x], lobby_list_response.owner[x]
            if (lobby_list_response.status[x] == "Invited"):
                invited_lobbies = invited_lobbies + [(lobby_list_response.lobbyIds[x],lobby_list_response.owner[x].email)]

    return render_template('create_game.html' ,invited_lobbies=invited_lobbies, friends_list=friends_list, game_type=game_type, lobby_id=lobby_id)

#not sure how to probe if I got invitations /get notifications (not sure we got time to implement notification service)
@app.route('/accept_invite/<int:game_type>/<int:lobby_id>', methods=['GET', 'POST'])
def accept_invite(game_type,lobby_id):
    print "accept invite"
    print "accepted lobbyId :", request.form['accepted_invite']
    print game_type
    print lobby_id
    friends_list = []

    try:
        accept_invite_response = lobbyservice.acceptLobbyInvite(AcceptLobbyInviteRequest(userId=session['userId'], lobbyId=int(request.form['accepted_invite'])))
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60

    #accept_invite_response = lobbyservice.acceptLobbyInvite(AcceptLobbyInviteRequest(userId=session['userId'], lobbyId=request.form['accepted_invite']))
    if (isinstance(accept_invite_response, AcceptLobbyInviteResponse)):
        print accept_invite_response
    friends_list = get_friends_list()
    return render_template('create_game.html',friends_list=friends_list,game_type=game_type,lobby_id=lobby_id)

# @app.route('/start_game/<int:game_type>/<int:lobby_id>', methods=['GET', 'POST'])
# def start_game(game_type,lobby_id):
#     print "start game"
#     print game_type
#     print lobby_id

@app.route('/remove_lobby/<int:game_type>/<int:lobby_id>', methods=['GET', 'POST'])
def remove_lobby(game_type,lobby_id):
    print "remove lobby"
    print game_type
    print lobby_id
    friends_list = []
    remove_lobby_response = lobbyservice.removeLobby(RemoveLobbyRequest(userId=session['userId'], lobbyId=lobby_id))
    if (isinstance(remove_lobby_response, RemoveLobbyResponse)):
        print remove_lobby_response
    friends_list = get_friends_list()
    return render_template('create_game.html',friends_list=friends_list,game_type=game_type,lobby_id=lobby_id)


@app.route('/get_friends/<int:game_type>',methods=['GET'])
def get_friends(game_type):
    print "get_friends test 2p"
    print game_type
    print session['userId']
    lobby_id = None
    friends_list = []
    try:
        response = lobbyservice.getLobbyId(CreateLobbyRequest(userId=session['userId'], gameType=game_type))
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60   
    #response = lobbyservice.getLobbyId(CreateLobbyRequest(userId=session['userId'], gameType=game_type))
    if (isinstance(response, CreateLobbyResponse)):
        print response
        lobby_id = response.lobbyId
    friends_list = get_friends_list()
    return render_template('create_game.html',friends_list=friends_list,game_type=game_type,lobby_id=lobby_id)

    
#************************ AWESOME ERROR FINDER ************************************
    # try:
    #     return render_template('create_game.html',friends_list=friends_list,game_type=game_type)
    # except:
    #     print "Exception in user code:"
    #     print '-'*60
    #     traceback.print_exc(file=sys.stdout)
    #     print '-'*60
    


#TODO: Quick Join 2/4 player Should be easy just call create lobbyId and use that to call start game directly 



@app.route('/start_game/<int:game_type>/<int:lobby_id>',methods=['GET', 'POST'])
def start_game(game_type,lobby_id):
    print "start game"
    print game_type
    print lobby_id
    gameId =""
    friends = []  
    if request.method == 'POST':
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                print key,":",value
                if not value ==''  :
                    friends=friends+[value]
        print friends
    print "test"
    try:
        start_game_response = lobbyservice.startGame(StartGameRequest(userId=session['userId'], lobbyId=lobby_id))
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60

    #start_game_response = lobbyservice.startGame(StartGameRequest(userId=session['userId'], lobbyId=lobby_id))
    if (isinstance(start_game_response, StartGameResponse)):
        print "test in isinstance"
        #gameId = str(start_game_response).split(":")[1]
        print start_game_response
        
        print "gameId:", gameId
        friends = [("asd@asd.se", 2)]
        
        players =[session['userId'],2]
        msg = CreateGameRequest(players=players)
        try:
            create_game_response = gameservice.send(msg)
            if isinstance(create_game_response, GameError):
                print "Error", create_game_response.description, " code: ", create_game_response.code 
            else:
                print "gameId", create_game_response.gameId
                gameId= create_game_response.gameId
        except TimeoutError as e:
            print "Timeout"

        #TODO: fetch friends from the gameId
        #friends = email string fetch with get_user_by_id 
        #also give userId
        
        board=[]
        return render_template('game_board.html',friends=friends, board=board, gameId=gameId, userId=session['userId'])
    else:
        return render_template('create_game.html',friends=friends,test=test, game_type=game_type)


