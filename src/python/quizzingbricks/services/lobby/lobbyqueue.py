#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

#imports
import random
import sys
import time
import cPickle as pickle
from python_linked_list import LinkedList, Node, removeFirst, addFirst, addLast, mergeNodes

#project imports
# from quizzingbricks.nuncius import NunciusService, expose
from quizzingbricks.common.protocol import CreateGameRequest, CreateGameResponse, GameError
from quizzingbricks.client.exceptions import TimeoutError
from quizzingbricks.client.games import GameServiceClient

#Other Dependencies
gameservice = GameServiceClient("tcp://*:1234")

#Variables
random_list_1 = [1]*5 + [2]*4 + [3]*1 	#gives a weighted randomness to the first queue
random_list_2 = [1]*1 + [2]*2 			#gives a weighted randomness to the second queue

#dev functions
def emptyqueues():
	global queue1
	global queue2
	global queue3
	global queue4
	global queue21
	global queue22
	queue1 = LinkedList()
	queue2 = LinkedList()
	queue3 = LinkedList()
	queue4 = LinkedList()
	queue21= LinkedList()
	queue22= LinkedList()
	dumpstate()


def display_list_length():
	print "queue 1: " +str(queue1.length)
	print "queue 2: " +str(queue2.length)
	print "queue 3: " +str(queue3.length)
	print "queue 4: " +str(queue4.length)
	print "queue 21: "+str(queue21.length)
	print "queue 22: "+str(queue22.length)

#Handle state
def dumpstate():
	pickle.dump( queue1, open( "queue1.save", "wb" ) )
	pickle.dump( queue2, open( "queue2.save", "wb" ) )
	pickle.dump( queue3, open( "queue3.save", "wb" ) )
	pickle.dump( queue4, open( "queue4.save", "wb" ) )
	pickle.dump( queue21,open( "queue21.save","wb" ) )
	pickle.dump( queue22,open( "queue22.save","wb" ) )

def loadstate():
	global queue1
	global queue2
	global queue3
	global queue4
	global queue21
	global queue22
	try:
		queue1 = pickle.load( open( "queue1.save", "rb" ) )
		queue2 = pickle.load( open( "queue2.save", "rb" ) )
		queue3 = pickle.load( open( "queue3.save", "rb" ) )
		queue4 = pickle.load( open( "queue4.save", "rb" ) )
		queue21= pickle.load( open( "queue21.save","rb" ) )
		queue22= pickle.load( open( "queue22.save","rb" ) )
	except IOError:
		queue1 = LinkedList()
		queue2 = LinkedList()
		queue3 = LinkedList()
		queue4 = LinkedList()
		queue21 = LinkedList()
		queue22 = LinkedList()
		dumpstate()


#Main program
def addtoqueue(id, max_players, current_players):
	if max_players == 2:
		print "in addtoqeue 2player"
		if len(current_players) == 1:
			addLast(queue21, id, max_players, current_players)
		elif len(current_players) == 2:
			addLast(queue22, id, max_players, current_players)

	elif max_players == 4:
		if len(current_players) == 1:
			addLast(queue1, id, max_players, current_players)
		elif len(current_players) == 2:
			addLast(queue2, id, max_players, current_players)
		elif len(current_players) == 3:
			addLast(queue3, id, max_players, current_players)
		elif len(current_players) == 4:
			addLast(queue4, id, max_players, current_players)
	dumpstate()

#Works
def worker():
	work = True
	kill = 0
	while (work):
		b = False
		a = fetch_lobby(1)
		if a:
			if fill_lobby_1(a):
				b = True

		a = fetch_lobby(2)
		if a:
			if fill_lobby_2(a):
				b = True

		a = fetch_lobby(3)
		if a:
			if fill_lobby_3(a):
				b = True

		a = fetch_lobby(4)
		if a:
			if fill_lobby_4(a):
				b = True
			
		a = fetch_lobby(21)
		if a:
			if fill_lobby_21(a):
				b = True

		a = fetch_lobby(22)
		if a:
			if fill_lobby_22(a):
				b = True

		#if fail 100 times in a row: execute
		if not b:
			kill+=1
			if kill == 100: 
				work = False
				print 'kill'
				dumpstate()
		else:
			kill=0

def update_lobby(lobby, queue):
	#inserts a lobby in the database
	#changes queue of lobby
	if queue == 1:
		addFirst(queue1, lobby.id, lobby.max_players, lobby.current_players)
	elif queue == 2:
		addFirst(queue2, lobby.id, lobby.max_players, lobby.current_players)
	elif queue == 3:
		addFirst(queue3, lobby.id, lobby.max_players, lobby.current_players)
	elif queue == 4:
		addFirst(queue4, lobby.id, lobby.max_players, lobby.current_players)
	elif queue == 21:
		addFirst(queue21, lobby.id, lobby.max_players, lobby.current_players)
	elif queue == 22:
		addFirst(queue22, lobby.id, lobby.max_players, lobby.current_players)

def merge_lobbies(a,b):
	#merges to lobbies into the first,
	#check if b exists
	if b:
		if set(a.current_players).intersection(set(b.current_players)):
			addtoqueue(b.id, b.max_players, b.current_players)
			return
		c = mergeNodes(a,b)
		return c
	else:
		return

def fetch_lobby(queue):
	#return the first element in the queue chosen 
	if queue == 1:
		return removeFirst(queue1)
	elif queue == 2:
		return removeFirst(queue2)
	elif queue == 3:
		return removeFirst(queue3)
	elif queue == 4:
		return removeFirst(queue4)
	elif queue == 21:
		return removeFirst(queue21)
	elif queue == 22:
		return removeFirst(queue22)

def start_game(lobby):
	#debugging:
	print "started lobby: ID: "+ str(lobby.id) +" max_players: "+ str(lobby.max_players) +" current_players: [%s]" % ", ".join(map(str, lobby.current_players))

	#send off the lobby to gameprocess
	players = lobby.current_players
	msg = CreateGameRequest(players=players)
	try:
		create_game_response = gameservice.send(msg, timeout=3000)
		if isinstance(create_game_response, GameError):
			print "Error", create_game_response.description, " code: ", create_game_response.code
			#we want to keep the lobby
			addtoqueue(lobby.id, lobby.max_players, lobby.current_players)
		else:
			print "gameId", create_game_response.gameId
			gameId= create_game_response.gameId
			dumpstate()

	except TimeoutError as e:
		print "Timeout"
		#we want to keep the lobby
		addtoqueue(lobby.id, lobby.max_players, lobby.current_players)

def fill_lobby_1(lobby):

	# possible choices
	# 3
	# 2
	# 1
	r = random.choice(random_list_1)
	#merge lobbies, if success: insert new lobby, else: insert old lobby, merge inserts the second lobby in another place if that happens
	if r == 1:
		#grab 1 from queue1
		ml = merge_lobbies(lobby, fetch_lobby(1))
		if ml:
			update_lobby(ml, 2)
			return True
		else:
			update_lobby(lobby, 1)
			return False
	elif r == 2:
		#grab 1 from queue2
		ml = merge_lobbies(lobby, fetch_lobby(2))
		if ml:
			update_lobby(ml, 3)
			return True
		else:
			update_lobby(lobby, 1)
			return False
	elif r == 3:
		#grab 1 from queue3
		ml = merge_lobbies(lobby, fetch_lobby(3))
		if ml:
			update_lobby(ml, 4)
			return True
		else:
			update_lobby(lobby, 1)
			return False

def fill_lobby_2(lobby):

	# possible choices
	# 2
	# 1
	if random.choice(random_list_2) == 1:
		#grab 1 from queue1
		ml = merge_lobbies(lobby, fetch_lobby(1))
		if ml:
			update_lobby(ml, 3)
			return True
		else:
			update_lobby(lobby, 2)
			return False
	else:
		#grab 1 from queue2
		ml = merge_lobbies(lobby, fetch_lobby(2))
		if ml:
			update_lobby(ml, 4)
			return True
		else:
			update_lobby(lobby, 2)
			return False

def fill_lobby_3(lobby):
	# possible choices
	# 1	
	ml = merge_lobbies(lobby, fetch_lobby(1))
	if ml:
		update_lobby(ml, 4)
		return True
	else:
		update_lobby(lobby, 3)
		return False

def fill_lobby_4(lobby):
	start_game(lobby)
	return True

def fill_lobby_21(lobby):
	#grab 1 from queue1
	ml = merge_lobbies(lobby, fetch_lobby(21))
	#insert into queue 2
	if ml:
		update_lobby(ml , 22)
		return True
	else:
		update_lobby(lobby, 21)
		return False

def fill_lobby_22(lobby):
	start_game(lobby)
	return True

loadstate()