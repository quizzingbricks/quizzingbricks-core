
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
import json

import sys, traceback

from collections import namedtuple
import zmq.green as zmq
from quizzingbricks.web import app, gameservice, zmq_ctx


from quizzingbricks.client.exceptions import TimeoutError
from quizzingbricks.common.protocol import (
    CreateGameRequest, CreateGameResponse, GameInfoRequest, GameInfoResponse,  \
    MoveRequest, MoveResponse, QuestionRequest, QuestionResponse, GameError, \
    AnswerRequest, AnswerResponse, GetMultipleUsersRequest, GetMultipleUsersResponse, \
    GetUserRequest, GetUserResponse,
    BoardChangePubSubMessage, NewRoundPubSubMessage,
    protocol_mapper)


@app.route('/active_games')
def active_games():  
    #TODO: fetch list of active games
    return render_template('active_games.html')

# @app.route('/choose_color', methods=["POST"])
# def choose_color():
#   token = request.form.get('token','None', type=str)
#   #session['player_color'] = token.upper()
#   #print session['player_color']
#   return jsonify(result=token)

@app.route('/game_info', methods=['POST'])
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
            print "game info this one", game_info_response.game
            return jsonify({ "gameId" : game_info_response.game.gameId,
                             "players" : [ { "userId" : player.userId,
                                            "state" : player.state,
                                            "x" : player.x,
                                            "y" : player.y,
                                            "question" : player.question,
                                            "alternatives" : [a for a in player.alternatives],
                                            "answeredCorrectly" : player.answeredCorrectly } for player in game_info_response.game.players ],
                             "board" : [b for b in game_info_response.game.board ]
                          })
    except TimeoutError as e:
        return jsonify(result = "Timeout")

@app.route('/get_question', methods=['POST'])
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
def game_board (gameId):
    friends = []
    board =[]
    friends =[("qwe@asd.se", 1)]
    #user_response= userservice.get_user(GetUserRequest(userId=1)
    #if(isinstance(user_response, GetUserResponse)):


    return render_template('game_board.html',friends=friends,board=board, gameId=gameId, userId=session['userId'])

@app.route("/game_board/<int:game_id>/events/")
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

            if isinstance(message, BoardChangePubSubMessage):
                ws.send(json.dumps({"type": "board_change", "payload": {"board": list(message.game.board)}}))
            elif isinstance(message, NewRoundPubSubMessage):
                ws.send(json.dumps({"type": "new_round", "payload": {}}))
            else:
                ws.send(json.dumps({"type": "unknown", "payload": {"msg_type": msg_type}})) # only used to debug
    abort(404) # only accessible from websockets