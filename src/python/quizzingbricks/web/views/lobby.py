
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify

import sys, traceback

from collections import namedtuple
from quizzingbricks.web import app, lobbyservice, gameservice
from quizzingbricks.web.views.utils import get_friends_list



from quizzingbricks.client.exceptions import TimeoutError
from quizzingbricks.common.protocol import (
    CreateLobbyRequest, CreateLobbyResponse, GetLobbyStateRequest, GetLobbyStateResponse, \
    AnswerLobbyInviteRequest, AnswerLobbyInviteResponse, InviteLobbyRequest, InviteLobbyResponse, \
    RemoveLobbyRequest, RemoveLobbyResponse, StartGameRequest, StartGameResponse,\
    GetLobbyListRequest, GetLobbyListResponse,CreateGameRequest, CreateGameResponse,\
    GameError
    )
from quizzingbricks.web import login_required


@app.route('/lobby_invite/<int:game_type>/<int:lobby_id>',methods=['GET', 'POST'])
@login_required
def lobby_invite(game_type,lobby_id):
    print "invite friends"
    friends = []  
    if request.method == 'POST':
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                if not value ==''  :
                    friends=friends+[int(value)]
    #print "friends id" ,friends
    lobby_invite_response = lobbyservice.invite_to_lobby(InviteLobbyRequest(userId=session['userId'],
                                                                            lobbyId=lobby_id, 
                                                                            invites=friends))
    if (isinstance(lobby_invite_response, InviteLobbyResponse)):
        print "lobby_invite_response", lobby_invite_response 
    return redirect(url_for('lobby',game_type=game_type, 
                                    lobby_id=lobby_id))

@app.route('/lobby_state/<int:game_type>/<int:lobby_id>', methods=['GET', 'POST'])
@login_required
def lobby_state(game_type, lobby_id):
    print "lobby state"  
    lobby_state_response = lobbyservice.get_lobby(GetLobbyStateRequest(lobbyId=lobby_id))
    if (isinstance(lobby_state_response, GetLobbyStateResponse)):
        pass
        #print "lobby state response", lobby_state_response
        # print "owner", lobby_state_response.lobby.owner
        # for member in lobby_state_response.lobby.lobbymembers:
        #     print "member", member.user.email


    return render_template('create_game.html',  owner=lobby_state_response.lobby.owner, 
                                                lobby_members=lobby_state_response.lobby.lobbymembers, 
                                                friends_list=get_friends_list(), 
                                                game_type=game_type, 
                                                lobby_id=lobby_id) 


@app.route('/remove_lobby/<int:game_type>/<int:lobby_id>', methods=['GET', 'POST'])
@login_required
def remove_lobby(game_type,lobby_id):
    print "remove lobby"
    print game_type
    print lobby_id

    remove_lobby_response = lobbyservice.remove_lobby(RemoveLobbyRequest(userId=session['userId'], lobbyId=lobby_id))
    if (isinstance(remove_lobby_response, RemoveLobbyResponse)):
        print "remove lobby respsone", remove_lobby_response

    return redirect(url_for('index'))


@app.route('/create_lobby/<int:game_type>',methods=['GET'])
@login_required
def create_lobby(game_type):
    print "get_friends test 2p"
    response = lobbyservice.create_lobby(CreateLobbyRequest(userId=session['userId'], gameType=game_type))
    #response = lobbyservice.getLobbyId(CreateLobbyRequest(userId=session['userId'], gameType=game_type))
    if (isinstance(response, CreateLobbyResponse)):
        pass
        #print response
    return redirect(url_for('lobby', game_type=game_type,
                                    lobby_id=response.lobbyId))

    
#************************ AWESOME ERROR FINDER ************************************
    # try:
    #     return render_template('create_game.html',friends_list=friends_list,game_type=game_type)
    # except:
    #     print "Exception in user code:"
    #     print '-'*60
    #     traceback.print_exc(file=sys.stdout)
    #     print '-'*60
    


#TODO: Quick Join 2/4 player Should be easy just call create lobbyId and use that to call start game directly 


@app.route('/lobby/<int:game_type>/<int:lobby_id>', methods=['GET'])
def lobby(game_type, lobby_id,):
    lobby_state_response = lobbyservice.get_lobby(GetLobbyStateRequest(lobbyId=lobby_id))
    if (isinstance(lobby_state_response, GetLobbyStateResponse)):
        pass
    return render_template('create_game.html',  lobby_members=lobby_state_response.lobby.lobbymembers, 
                                                friends_list=get_friends_list(),
                                                game_type=game_type,
                                                lobby_id=lobby_id)



@app.route('/start_game/<int:game_type>/<int:lobby_id>',methods=['GET', 'POST'])
@login_required
def start_game(game_type,lobby_id):
    print "start game"
    start_game_response = lobbyservice.start_game(StartGameRequest(userId=session['userId'], lobbyId=lobby_id))
    if (isinstance(start_game_response, StartGameResponse)):
        pass
    return redirect(url_for('index'))




#********************************* Lobby List *****************************************************

@app.route('/lobby_list', methods=['GET', 'POST'])
@login_required
def lobby_list():
    print "lobby list"  
  
    lobby_list_response = lobbyservice.get_lobbies(GetLobbyListRequest(userId=session['userId']))
    if (isinstance(lobby_list_response, GetLobbyListResponse)):
        #print "lobby list response", lobby_list_response
        pass
    return render_template('lobby_list.html',  lobby_list=lobby_list_response.lobbies, 
                                                friends_list=get_friends_list())

#not sure how to probe if I got invitations /get notifications (not sure we got time to implement notification service)
@app.route('/accept_invite/', methods=['GET', 'POST'])
@login_required
def accept_invite():
    print "accept invite"
    answer=""
    if(request.form.get('accepted_invite') == None):
        answer="deny"
    else:
        answer="accept"

    answer_invite_response = lobbyservice.answer_lobby_invite(AnswerLobbyInviteRequest( userId=session['userId'], 
                                                                                        lobbyId=int(request.form['invite_lobby_id']),
                                                                                        answer=answer))
    if (isinstance(answer_invite_response, AnswerLobbyInviteResponse)):
        pass
    return redirect(url_for('lobby_list'))


