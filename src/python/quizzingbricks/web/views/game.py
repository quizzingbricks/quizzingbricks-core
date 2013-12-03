
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
import json

import sys, traceback

from collections import namedtuple
import zmq.green as zmq
from quizzingbricks.web import app, gameservice, zmq_ctx, userservice


from quizzingbricks.client.exceptions import TimeoutError
from quizzingbricks.common.protocol import (
    CreateGameRequest, CreateGameResponse, GameInfoRequest, GameInfoResponse,  \
    MoveRequest, MoveResponse, QuestionRequest, QuestionResponse, GameError, \
    AnswerRequest, AnswerResponse, GetMultipleUsersRequest, GetMultipleUsersResponse, \
    GetUserRequest, GetUserResponse, PlayerStateChangePubSubMessage, NewRoundPubSubMessage, \
    GameListRequest, GameListResponse,protocol_mapper )
from quizzingbricks.web import login_required


@app.route('/active_games')
@login_required
def active_games():  
    #TODO: fetch list of active games
    msg = GameListRequest()
    msg.userId = session['userId']
    try:
        game_list_response = gameservice.send(msg)
        if isinstance(game_list_response, GameError):
            return jsonify(result=(game_list_response.description, game_list_response.code))
        else:

            games=[]
            for game in game_list_response.games:
                playerIds=[]
                for player in game.players:
                    if player.userId != session['userId']:
                        playerIds.append(player.userId)
                multiple_player_response = userservice.get_multiple_users(GetMultipleUsersRequest(userIds=playerIds))
                if(isinstance(multiple_player_response, GetMultipleUsersResponse)):
                    currentGame = (game, list(multiple_player_response.users))
                    games.append(currentGame)
            return render_template('active_games.html', games=games)
                    
            #print game_list_response
            # friends_list=[]
            # memberIds = []
            # for game in game_list_response.games:
            #     for player in game.players:
            #     if player.userId != session['userId']:
            #         memberIds.append(player.userId)
            # multiple_player_response = userservice.get_multiple_users(GetMultipleUsersRequest(userIds=memberIds))
            # if (isinstance(multiple_player_response, GetMultipleUsersResponse)):
            #     print multiple_player_response
            #     pass


            # friends_list.append(namedtuple(game)list(multiple_player_response.users))
            # return render_template('active_games.html', games= game_list_response.games ) 
            #print "game info this one", game_list_response.games
            #return jsonify({"games":[{ "gameId" : game.gameId} for game in game_list_response.games] }) 
                             # "players" : [ { "userId" : player.userId,
                             #                "state" : player.state,
                             #                "x" : player.x,
                             #                "y" : player.y,
                             #                "question" : player.question,
                             #                "alternatives" : [a for a in player.alternatives],
                             #                "answeredCorrectly" : player.answeredCorrectly } for player in game_info_response.game.players ],
                             # "board" : [b for b in game_info_response.game.board ]
                             #  })
        
    except TimeoutError as e:
        return jsonify(result = "Timeout")
    

# @app.route('/choose_color', methods=["POST"])
# def choose_color():
#   token = request.form.get('token','None', type=str)
#   #session['player_color'] = token.upper()
#   #print session['player_color']
#   return jsonify(result=token)

@app.route('/game_info', methods=['POST'])
@login_required
def game_info():
    print "game info "
    gameId = request.form.get('gameId',0, type=int)
    msg = GameInfoRequest()
    msg.gameId = gameId
    try:
        game_info_response = gameservice.send(msg)
        if isinstance(game_info_response, GameError):
            return jsonify(result=(game_info_response.description, game_info_response.code))
        else:
            return jsonify({ "gameId" : game_info_response.game.gameId,
                             "players" : [ { "userId" : player.userId,
                                            "state" : player.state,
                                            "x" : player.x,
                                            "y" : player.y,
                                            "score": player.score,
                                            #"question" : player.question,
                                            #"alternatives" : [a for a in player.alternatives],
                                            "answeredCorrectly" : player.answeredCorrectly } for player in game_info_response.game.players ],
                             "board" : [b for b in game_info_response.game.board ]
                          })
    except TimeoutError as e:
        return jsonify(result = "Timeout")

@app.route('/get_question', methods=['POST'])
@login_required
def get_question():
    print "get question"
    gameId = request.form.get('gameId',0, type=int)
    msg = QuestionRequest()
    msg.gameId = gameId
    msg.userId = session['userId']
    #return jsonify({ "question" : "Starts the alphabet?", "alternatives" : [a for a in ["a","b","c","d"]] }) 
    #added in order to be able to have a proper message to parse 
    try:
        get_question_response = gameservice.send(msg)
        if isinstance(get_question_response, GameError):
            return jsonify(result=(get_question_response.description, get_question_response.code)) 
        else:
            return jsonify({ "isQuestion": True, "question" : get_question_response.question, "alternatives" : [a for a in get_question_response.alternatives] })
    except TimeoutError as e:
        return jsonify(result = "Timeout")

@app.route('/submit_answer', methods=['POST'])
@login_required
def submit_answer():
    print "submit answer"
    gameId = request.form.get('gameId',0, type=int)
    answer = request.form.get('answer',0, type=int)
    print "answer", answer
    msg = AnswerRequest()
    msg.gameId = gameId
    msg.userId = session['userId']
    msg.answer = answer
    # if (answer==1):
    #     return jsonify({ "isCorrect" : True })
    # else:
    #     return jsonify({ "isCorrect" : False })
    try:
        submit_answer_response = gameservice.send(msg)
        if isinstance(submit_answer_response,GameError):
            return jsonify(result=(submit_answer_response.description, submit_answer_response.code))
        else:
            return jsonify({ "isCorrect" : submit_answer_response.isCorrect })
    except TimeoutError as e:
        return jsonify(result = "Timeout")



@app.route('/make_move', methods=["POST"])
@login_required
def tile_placement():
    print "game board in run_web"
    gameId = request.form.get('gameId',0, type=int)
    x = request.form.get('x', 0, type=int)
    y = request.form.get('y', 0, type=int)
    print "gameId", gameId
    print "userId", session['userId']
    print "x: ",x
    print "y: ",y
    print "before msg"

    msg = MoveRequest()
    msg.x       = x
    msg.y       = y
    msg.gameId   = gameId
    msg.userId  = session['userId']
    try:
        player_move_response = gameservice.send(msg)
        if(isinstance(player_move_response,GameError)):
            return jsonify(result=(player_move_response.description, player_move_response.code))
        else:
            return jsonify(result ="Move sent")
    except TimeoutError as e:
        return jsonify(result = "Timeout")

   # print session['username']
   # return jsonify(result =(x,y))



@app.route('/game_board/<int:gameId>',methods=["GET"])          #changed so I can test a gameId with
@login_required
def game_board (gameId):
    memberIds = []



    msg = GameInfoRequest()
    msg.gameId = gameId
    try:
        game_info_response = gameservice.send(msg)
        if isinstance(game_info_response, GameError):
            return jsonify(result=(game_info_response.description, game_info_response.code))
        else:
            for player in game_info_response.game.players:
                if player.userId != session['userId']:
                    memberIds.append(player.userId)
            multiple_player_response = userservice.get_multiple_users(GetMultipleUsersRequest(userIds=memberIds))
            if (isinstance(multiple_player_response, GetMultipleUsersResponse)):
                print multiple_player_response
                pass

            # return jsonify({ "gameId" : game_info_response.game.gameId,
            #                  "players" : [ { "userId" : player.userId,
            #                                 "state" : player.state,
            #                                 "x" : player.x,
            #                                 "y" : player.y,
            #                                 "question" : player.question,
            #                                 "alternatives" : [a for a in player.alternatives],
            #                                 "answeredCorrectly" : player.answeredCorrectly } for player in game_info_response.game.players ],
            #                  "board" : [b for b in game_info_response.game.board ]
            #               })
    except TimeoutError as e:
        return jsonify(result = "Timeout")

    return render_template('game_board.html',friends=list(multiple_player_response.users), gameId=gameId, userId=session['userId'])

@app.route("/game_board/<int:game_id>/events/")
@login_required
def game_listener(game_id):
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']

        sock = zmq_ctx.socket(zmq.SUB)
        sock.connect("tcp://*:5202")
        sock.setsockopt(zmq.SUBSCRIBE, "game-%d" % game_id)

        while True:
            print "started websocket listener"
            game_id, msg_type, msg = sock.recv_multipart()
            cls = protocol_mapper.get(int(msg_type))
            message = cls.FromString(msg)
            print "deseralized type: %s" % message.__class__.__name__

            if isinstance(message, PlayerStateChangePubSubMessage):
                ws.send(json.dumps({"type": "player_change", "payload": {"player": {"id": message.player.userId, "state": message.player.state, "score": message.player.score}}}))
            elif isinstance(message, NewRoundPubSubMessage):
                ws.send(json.dumps({
                    "type": "board_change",
                    "payload": {
                        "board": list(message.game.board),
                        "players": [
                            {"id": player.userId, "state": player.state, "score": player.score}
                            for player in message.game.players
                        ]
                    },
                }))
            else:
                ws.send(json.dumps({"type": "unknown", "payload": {"msg_type": msg_type}})) # only used to debug
    abort(404) # only accessible from websockets