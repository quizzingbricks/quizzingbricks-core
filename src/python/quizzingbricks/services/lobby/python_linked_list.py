#http://www.openbookproject.net/thinkcs/python/english2e/ch18.html



class LinkedList:
	def __init__(self):
		self.length = 0
		self.head   = None

class Node:
	def __init__(self, id=None, max_players = None, current_players = None, next=None):
		self.id = id
		self.max_players = max_players
		self.current_players = current_players
		self.next  = next

def removeFirst(self):
	if self.length == 0: return
	first = self.head
	
	if self.length == 1:
		self.length = 0
		self.head = None
		return first
	
	second = self.head.next
	self.head = second
	self.length -=1
	return first

def addFirst(self, id, max_players, current_players):
	node = Node(id, max_players, current_players)
	node.next = self.head
	self.head = node
	self.length +=1

def addLast(self, id, max_players, current_players):
	node = Node(id, max_players, current_players)
	nextnode = self.head
	self.length +=1
	
	if nextnode == None:
		node.next = self.head
		self.head = node
	else:
		while nextnode:
			if nextnode.next == None:
				nextnode.next = node
				return
			else:
				nextnode = nextnode.next

def addRandom(self, id, max_players, current_players):
	return

def mergeNodes(nodeA,nodeB):
	nodeA.current_players=nodeA.current_players+nodeB.current_players
	return nodeA

