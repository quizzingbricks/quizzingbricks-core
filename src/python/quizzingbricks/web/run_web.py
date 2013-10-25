from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify

from quizzingbricks.client.exceptions import TimeoutError
from quizzingbricks.client.users import UserServiceClient
from quizzingbricks.common.protocol import (
    LoginRequest, LoginResponse, RegistrationRequest, RegistrationResponse
)

#configuration

USERNAME = 'admin'
PASSWORD = 'pass'
SECRET_KEY = 'development key'

userservice = UserServiceClient("tcp://*:5551")

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

@app.route('/get_friends',methods=['GET', 'POST'])
def get_friends():
    friends_list = None
    if request.method == 'POST':
        test_friend_1 = "Anton"
        test_friend_2 = "David"
        test_friend_3 = "Linus"
        test_friend_4 = "William" 
        test_friend_5 = "Niklas"
        friends_list=[test_friend_1,test_friend_2,test_friend_3,test_friend_4,test_friend_5]
        return render_template('create_game.html',friends_list=friends_list)
    else:
        test_friend_1 = "Anton"
        test_friend_2 = "David"
        test_friend_3 = "Linus"
        test_friend_4 = "William" 
        test_friend_5 = "Niklas"
        friends_list=[test_friend_1,test_friend_2,test_friend_3,test_friend_4,test_friend_5]
        return render_template('create_game.html',friends_list=friends_list)

@app.route('/create_game',methods=['GET', 'POST'])
def create_game():
    print "test"
    friends = []
    test = []  


    if request.method == 'POST':
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                print key,":",value
                if not value ==''  :
                    friends=friends+[value]
        print friends
        return render_template('test_board.html',friends=friends,test=test)
    else:
        return render_template('create_game.html',friends=friends,test=test)

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
            responce = userservice.create_user(RegistrationRequest(email=request.form['email'], password=request.form['password1']),1000)
            if (isinstance(responce, RegistrationResponse)):
                error= str(responce.userId)
                return render_template('index.html',error=error)
            else:
                error= responce.message
                return render_template('register_user.html',error=error)
    return render_template('register_user.html')

#else:
#	flash('You have registerd')
#	return redirect(url_for('/'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        responce = userservice.authenticate(LoginRequest(email=request.form['email'], password=request.form['password']),1000)
        if (isinstance(responce, LoginResponse)):
            session['userId'] = str(responce.userId)
            session['logged_in'] = True
        else:
            error=responce.message
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