from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify

import sys, traceback

from quizzingbricks.client.exceptions import TimeoutError
from quizzingbricks.client.users import UserServiceClient
from quizzingbricks.client.lobby import LobbyServiceClient
from quizzingbricks.client.friends import FriendServiceClient
from quizzingbricks.common.protocol import (
    LoginRequest, LoginResponse, RegistrationRequest, RegistrationResponse , \
     CreateLobbyRequest, CreateLobbyResponse, GetFriendsRequest, GetFriendsResponse, \
     AddFriendRequest, AddFriendResponse, RemoveFriendRequest, RemoveFriendResponse   
)

#configuration

USERNAME = 'admin'
PASSWORD = 'pass'
SECRET_KEY = 'development key'

userservice = UserServiceClient("tcp://*:5551")
lobbyservice = LobbyServiceClient("tcp://*:5552")
friendservice = FriendServiceClient("tcp://*:5553")


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
            add_friend_response = friendservice.add_Friend(AddFriendRequest(friend_email=friend_Email))
            if (isinstance(add_friend_response, AddFriendResponse)):
                #print "add response", add_friend_response
                friends_response = friendservice.get_Friends_list(GetFriendsRequest(userId=1))  #hard coded userId
                if (isinstance(friends_response,GetFriendsResponse)):
                    for friend in friends_response.friends_list:
                        friends_list=friends_list+ [friend]
                    return render_template('friends_list.html',friends_list=friends_list)
        else:
            friends_response = friendservice.get_Friends_list(GetFriendsRequest(userId=1))  #hard coded userId
            if (isinstance(friends_response,GetFriendsResponse)):
                for friend in friends_response.friends_list:
                    friends_list=friends_list+ [friend]
                return render_template('friends_list.html',friends_list=friends_list, error="Must fill in email of user you want to friend")   
    else:
        friends_response = friendservice.get_Friends_list(GetFriendsRequest(userId=1))  #hard coded userId
        if (isinstance(friends_response,GetFriendsResponse)):
            for friend in friends_response.friends_list:
                friends_list=friends_list+ [friend]
            return render_template('friends_list.html',friends_list=friends_list)    

@app.route('/remove_friend', methods=['GET', 'POST'])
def remove_friend():
    friends_list = []
    if request.method == 'POST':    # removes selected friend and fetches the rest of the friendslist again if more is to be removed
        try:
            remove_friend_response = friendservice.remove_Friend(RemoveFriendRequest(friend_email=request.form['friend']))
            if (isinstance(remove_friend_response, RemoveFriendResponse)):
                print "remove response", remove_friend_response
                friends_response = friendservice.get_Friends_list(GetFriendsRequest(userId=1))  #hard coded userId
                if (isinstance(friends_response,GetFriendsResponse)):
                    #print friends_response
                    for friend in friends_response.friends_list:
                        #print friend
                        friends_list=friends_list+ [friend]
                    return render_template('friends_list.html',friends_list=friends_list)
        except: #no radio buttons selected
            friends_response = friendservice.get_Friends_list(GetFriendsRequest(userId=1))  #hard coded userId
            if (isinstance(friends_response,GetFriendsResponse)):
                #print friends_response
                for friend in friends_response.friends_list:
                    #print friend
                    friends_list=friends_list+ [friend]
                return render_template('friends_list.html',friends_list=friends_list, error="Must select radio button")

    else:
        friends_response = friendservice.get_Friends_list(GetFriendsRequest(userId=1))  #hard coded userId
        if (isinstance(friends_response,GetFriendsResponse)):
            #print friends_response
            for friend in friends_response.friends_list:
                #print friend
                friends_list=friends_list+ [friend]
            return render_template('friends_list.html',friends_list=friends_list)

@app.route('/get_friends/<int:game_type>',methods=['GET'])
def get_friends_2p(game_type):
    print "get_friends test 2p"
    print game_type
    lobby_id = None
    friends_list = []
    
    response = lobbyservice.getLobbyId(CreateLobbyRequest(userId=1, gameType=game_type))
    if (isinstance(response, CreateLobbyResponse)):
        print response
        lobby_id = response.lobbyId

    friends_response = friendservice.get_Friends_list(GetFriendsRequest(userId=1))  #hard coded userId
    if (isinstance(friends_response,GetFriendsResponse)):
        print friends_response
        for friend in friends_response.friends_list:
            print friend
            friends_list=friends_list+ [friend]
        return render_template('create_game.html',friends_list=friends_list,game_type=game_type,lobby_id=lobby_id)

    
#************************ AWESOME ERROR FINDER ************************************
    # try:
    #     return render_template('create_game.html',friends_list=friends_list,game_type=game_type)
    # except:
    #     print "Exception in user code:"
    #     print '-'*60
    #     traceback.print_exc(file=sys.stdout)
    #     print '-'*60
    






@app.route('/create_game/<int:game_type>',methods=['GET', 'POST'])
def create_game(game_type):
    friends = []  
    if request.method == 'POST':
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                print key,":",value
                if not value ==''  :
                    friends=friends+[value]
        print friends
        return render_template('test_board.html',friends=friends)
    else:
        return render_template('create_game.html',friends=friends,test=test, game_type=game_type)



@app.route('/active_games')
def active_games():  
    return render_template('active_games.html')

@app.route('/choose_color', methods=["POST"])
def choose_color():
	token = request.form.get('token','None', type=str)
	#session['player_color'] = token.upper()
	#print session['player_color']
	return jsonify(result=token)



@app.route('/game_board',methods=["GET"])
def game_board ():
	return render_template('game_board.html')

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
            session['userId'] = str(response.userId)
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



@app.route('/game_board', methods=["POST"])
def tile_placement():
    x = request.form.get('x', 0, type=int)
    y = request.form.get('y', 0, type=int)
   # print session['username']
    return jsonify(result =(x,y))

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