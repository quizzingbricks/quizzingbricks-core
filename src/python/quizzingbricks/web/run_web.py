# from flask import Flask, request, session, g, redirect, url_for, \
#      abort, render_template, flash, jsonify

# import sys, traceback

# from collections import namedtuple

# import quizzingbricks.web.views

# from quizzingbricks.web import app

# from quizzingbricks.client.exceptions import TimeoutError
# from quizzingbricks.client.users import UserServiceClient
# from quizzingbricks.client.lobby import LobbyServiceClient
# from quizzingbricks.client.friends import FriendServiceClient
# from quizzingbricks.client.games import GameServiceClient
# from quizzingbricks.common.protocol import (
#     LoginRequest, LoginResponse, RegistrationRequest, RegistrationResponse , \
#      CreateLobbyRequest, CreateLobbyResponse, GetFriendsRequest, GetFriendsResponse, \
#      AddFriendRequest, AddFriendResponse, RemoveFriendRequest, RemoveFriendResponse, \
#      GetLobbyStateRequest, GetLobbyStateResponse, AcceptLobbyInviteRequest, AcceptLobbyInviteResponse, \
#      InviteLobbyRequest, InviteLobbyResponse, RemoveLobbyRequest, RemoveLobbyResponse, \
#      StartGameRequest, StartGameResponse, GetLobbyListRequest, GetLobbyListResponse, \
#      CreateGameRequest, CreateGameResponse, GameInfoRequest, GameInfoResponse,  \
#      MoveRequest, MoveResponse, QuestionRequest, QuestionResponse, GameError, \
#      AnswerRequest, AnswerResponse, GetMultipleUsersRequest, GetMultipleUsersResponse, \
#      GetUserRequest, GetUserResponse )


    

# #configuration

# USERNAME = 'admin'
# PASSWORD = 'pass'


# userservice = UserServiceClient("tcp://*:5551")
# lobbyservice = LobbyServiceClient("tcp://*:5552")
# friendservice = FriendServiceClient("tcp://*:5553")
# gameservice = GameServiceClient("tcp://*:1234")










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






# @app.route('/test_board',methods=["GET"])
# def test_board ():
#     return render_template('test_board.html')




# @app.route('/test_board', methods=["POST"])
# def test_tile_placement():
#     x = request.form.get('x', 0, type=int)
#     y = request.form.get('y', 0, type=int)
#     #print "test before"
#     #print session.__dict__
#     #print "test after"
#     #print session['logged_in']
#     return jsonify(result =(x,y))





# if __name__ == '__main__':
#     app.run(host='0.0.0.0',debug=True)
# #    app.run(debug=True)

# def get_friends_list():
#     friends_list=[]
#     Friend = namedtuple("Friend", ("id", "email"))
#     friends_response = friendservice.get_friends(GetFriendsRequest(userId=session['userId']), timeout=5000)  #hard coded userId
#     if (isinstance(friends_response,GetFriendsResponse)):
#         for friend in friends_response.friends:
#             friends_list.append(Friend(friend.id, friend.email))
#     return friends_list

