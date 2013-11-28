
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify

import sys, traceback

from collections import namedtuple
from quizzingbricks.web import app, userservice



from quizzingbricks.client.users import UserServiceClient
from quizzingbricks.common.protocol import (
    LoginRequest, LoginResponse, RegistrationRequest, RegistrationResponse
    )


#userservice = UserServiceClient("tcp://*:5551")


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
    print "hmm"
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


