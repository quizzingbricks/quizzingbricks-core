from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify

import sys, traceback

from quizzingbricks.client.exceptions import TimeoutError
from quizzingbricks.client.users import UserServiceClient
from quizzingbricks.client.lobby import LobbyServiceClient
from quizzingbricks.client.friends import FriendServiceClient
from quizzingbricks.client.games import GameServiceClient
from quizzingbricks.common.protocol import (
    LoginRequest, LoginResponse, RegistrationRequest, RegistrationResponse , \
     CreateLobbyRequest, CreateLobbyResponse, GetFriendsRequest, GetFriendsResponse, \
     AddFriendRequest, AddFriendResponse, RemoveFriendRequest, RemoveFriendResponse, \
     GetLobbyStateRequest, GetLobbyStateResponse, AcceptLobbyInviteRequest, AcceptLobbyInviteResponse, \
     InviteLobbyRequest, InviteLobbyResponse, RemoveLobbyRequest, RemoveLobbyResponse, \
     StartGameRequest, StartGameResponse, GetLobbyListRequest, GetLobbyListResponse, \
     CreateGameRequest, CreateGameResponse, GameInfoRequest, GameInfoResponse,  \
     MoveRequest, MoveResponse, QuestionRequest, QuestionResponse, GameError, \
     AnswerRequest, AnswerResponse, GetMultipleUsersRequest, GetMultipleUsersResponse, \
     GetUserRequest, GetUserResponse )
    

#configuration

USERNAME = 'admin'
PASSWORD = 'pass'
SECRET_KEY = 'development key'

userservice = UserServiceClient("tcp://*:5551")
lobbyservice = LobbyServiceClient("tcp://*:5552")
friendservice = FriendServiceClient("tcp://*:5553")
gameservice = GameServiceClient("tcp://*:1234")

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact')
def contact():	
	return render_template('contact.html')


@app.route('/add_friend', methods=['GET', 'POST'])
def add_friend():
    friends_list = []
    if request.method == 'POST':
        friend_Email = request.form['friend_email']
        if(friend_Email!= ""):
            add_friend_response = friendservice.add_friend(AddFriendRequest(userId=session['userId'],friend_email=friend_Email))
            if (isinstance(add_friend_response, AddFriendResponse)):
                #print "add response", add_friend_response
                friends_list = get_friends_list()
                return render_template('friends_list.html',friends_list=friends_list)
        else:
            friends_list = get_friends_list()
            return render_template('friends_list.html',friends_list=friends_list, error="Must fill in email of user you want to add")   
    else:
        friends_list = get_friends_list()
        return render_template('friends_list.html',friends_list=friends_list)    

@app.route('/remove_friend', methods=['GET', 'POST'])
def remove_friend():
    friends_list = []
    if request.method == 'POST':    # removes selected friend and fetches the rest of the friendslist again if more is to be removed
        try:
            remove_friend_response = friendservice.remove_friend(RemoveFriendRequest(userId =session['userId'],friend_email=request.form['friend']))
            if (isinstance(remove_friend_response, RemoveFriendResponse)):
                print "remove response", remove_friend_response
                friends_list = get_friends_list()
                return render_template('friends_list.html',friends_list=friends_list)
        except: #no radio buttons selected
            friends_list = get_friends_list()
            return render_template('friends_list.html',friends_list=friends_list, error="Must select radio button")

    else:
        friends_list = get_friends_list()
        return render_template('friends_list.html',friends_list=friends_list)

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
        friends = [("David@test.se", 2)]
        
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




# @app.route('/game_info/<int:game_id>', methods=['GET','POST'])
# def game_info(game_id):
#     print "game info"
#     print game_id
#     friends = []
#     board = []
#     friend1 = ("David@test.se", 2)
#     friend2 = ("Anton@test.se", 25)
#     friends = [friend1,friend2]
#     for x in range(0,64):
#         if (x > 40):
#             board = board +[1]
#         elif (x<20):
#             board = board +[2]
#         else:
#             board = board + [0]
#     return render_template('game_board.html',friends=friends, gameId=game_id, board=board, userId=session['userId'])




@app.route('/active_games')     
def active_games():  
    #TODO: fetch list of active games
    return render_template('active_games.html')

# @app.route('/choose_color', methods=["POST"])
# def choose_color():
# 	token = request.form.get('token','None', type=str)
# 	#session['player_color'] = token.upper()
# 	#print session['player_color']
# 	return jsonify(result=token)

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
            print "game info", game_info_response
            return jsonify({ "gameId" : game_info_response.gameId,
                             "players" : [ { "userId" : player.userId,
                                            "state" : player.state,
                                            "x" : player.x,
                                            "y" : player.y,
                                            "question" : player.question,
                                            "alternatives" : [a for a in player.alternatives],
                                            "answeredCorrectly" : player.answeredCorrectly } for player in game_info_response.players ],
                             "board" : [b for b in game_info_response.board ]
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
            return jsonify({ "question" : get_question_response.question, "alternatives" : [a for a in get_question_response.alternatives] })
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

@app.route('/test_board',methods=["GET"])
def test_board ():
	return render_template('test_board.html')	

@app.route('/register_user',methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        if(request.form['password1']!=request.form['password2']):
            error = "Password not the same"
            return render_template('register_user.html',error=error)
        else:
            response = userservice.create_user(RegistrationRequest(email=request.form['email'], password=request.form['password1']),1000)
            if (isinstance(response, RegistrationResponse)):
                error= str(response.userId)
                return render_template('index.html',error=error)
            else:
                error= response.message
                return render_template('register_user.html',error=error)
    return render_template('register_user.html')

#else:
#	flash('You have registerd')
#	return redirect(url_for('/'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        response = userservice.authenticate(LoginRequest(email=request.form['email'], password=request.form['password']),1000)
        if (isinstance(response, LoginResponse)):
            session['userId'] = response.userId
        #session['userId'] = 98789
            session['logged_in'] = True
        else:
            error=response.message
 
 
 #       if request.form['username'] != app.config['USERNAME']:
 #           error = 'Invalid username'
 #       elif request.form['password'] != app.config['PASSWORD']:
 #           error = 'Invalid password'
 #       else:
 #           
#            session['username'] = request.form['username']

  #          flash('You were logged in')
   #         return redirect(url_for('index'))
    return render_template('index.html', error=error)

@app.route('/logout')
def logout():

    session.pop('logged_in', None)
    session.pop('userId', None)
    #session.pop('username', None)
    #session.pop('player_color', None)
    #session.pop('modified', None)
    #session.pop('on_update', None)
    #session.clear()
    print "inside logout"
    flash('You were logged out')
    return redirect(url_for('index'))





@app.route('/test_board', methods=["POST"])
def test_tile_placement():
    x = request.form.get('x', 0, type=int)
    y = request.form.get('y', 0, type=int)
    #print "test before"
    #print session.__dict__
    #print "test after"
    #print session['logged_in']
    return jsonify(result =(x,y))





if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
#    app.run(debug=True)

def get_friends_list():
    friends_list=[]
    friends_response = friendservice.get_friends(GetFriendsRequest(userId=session['userId']), timeout=5000)  #hard coded userId
    if (isinstance(friends_response,GetFriendsResponse)):
        for friend in friends_response.friends:
            friends_list=friends_list+ [friend.email]
    return friends_list

