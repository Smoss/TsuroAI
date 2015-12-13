import copy, sys
tiles = [[[(0, 1), (2, 3), (4, 5), (6, 7)],
         [(0, 7), (1, 6), (2, 3), (4, 5)],
		 [(4, 5), (6, 3), (7, 0), (1, 2)],
		 [(0, 7), (1, 2), (3, 4), (5, 6)],
		 [(0, 6), (1, 7), (2, 3), (4, 5)],

		 [(0, 1), (4, 5), (2, 7), (3, 6)],
		 [(0, 1), (4, 5), (2, 6), (3, 7)],
		 [(0, 6), (1, 2), (3, 7), (4, 5)],
		 [(2, 6), (3, 4), (5, 7), (0, 1)],		 
		 [(6, 0), (7, 5), (1, 2), (3, 4)],

		 [(4, 3), (5, 7), (6, 1), (2, 0)],
		 [(6, 1), (7, 3), (0, 2), (4, 5)],
		 [(4, 5), (6, 3), (7, 1), (0, 2)],
		 [(4, 5), (6, 2), (7, 1), (0, 3)],
		 [(4, 5), (6, 1), (7, 2), (0, 3)],

		 [(1, 2), (0, 3), (5, 6), (4, 7)],
		 [(0, 3), (1, 2), (7, 5), (6, 4)],
		 [(1, 2), (0, 4), (3, 6), (5, 7)],
		 [(2, 1), (3, 7), (4, 0), (5, 6)],
		 [(2, 3), (4, 6), (5, 0), (7, 1)],

		 [(5, 0), (4, 3), (7, 2), (1, 6)],
		 [(4, 6), (5, 0), (7, 3), (1, 2)],
		 [(6, 4), (5, 0), (7, 2), (1, 3)],
		 [(0, 5), (1, 3), (2, 6), (4, 7)],
		 [(2, 6), (3, 1), (4, 0), (5, 7)],

		 [(2, 0), (3, 1), (4, 6), (5, 7)],
		 [(0, 5), (1, 4), (2, 7), (3, 6)],
		 [(2, 6), (3, 7), (1, 4), (0, 5)],
		 [(0, 4), (1, 5), (2, 6), (3, 7)],
		 [(6, 2), (7, 4), (0, 3), (1, 5)],

		 [(6, 4), (7, 2), (5, 1), (0, 3)],
		 [(0, 2), (1, 5), (7, 3), (6, 4)],
		 [(0, 3), (1, 6), (2, 4), (5, 7)],
		 [(0, 6), (1, 3), (2, 4), (5, 7)],
		 [(0, 3), (1, 6), (2, 5), (4, 7)]]


positions_adders = {0 : (-1, 0), 1 : (-1, 0), 2 : (0, 1), 3 : (0, 1), 4 : (1, 0), 5 : (1, 0), 6 : (0, -1), 7 : (0, -1)}		
"""
returns:
	-1 - some error somehow
    0 - all good, turn taken
    1 - turn skipped, already dead
"""
class TsuroGame():
	def __init__(self, players):
		self.players = players
		self.board = TsuroBoard()
		self.tiles = [TsuroTile(tileInfo) for tileInfo in tiledata]

	def transform(self, tile, location):
		newBoard = copy.deepCopy(self.board)
		newBoard.placeTile(tile, location)
		return newBoard

	def playCard(self, tile, location):
		self.board = self.transform(tile, location)

	def gameOver(self):
		livingPlayerCount = len(filter((lambda p: p.alive()), self.players))
		return livingPlayerCount == 1 or livingPlayerCount == 0

	def playTurn(self, turn):
		currentPlayer = self.players[turn % len(self.players)]
		if not currentPlayer.alive():
			print "Player %s is eliminated, skipping their turn"
			return 1
		else:
			selectedTile = currentPlayer.chooseTile()
			self.playCard(selectedTile)
			self.moveAllPlayers()
			self.wrapUpTurn(currentPlayer)

	def moveAllPlayers():
		for player in filter(lambda p: player.alive(), self.players):
			newLocation = self.board.followPath(player.location)
			player.location = (newLocation[1][0], newLocation[1][1], newLocation[2])
			if not newLocation[0]:
				print "Player %s has been eliminated"
				self.handlePlayerDeath(player)
	""" 
	Anything after a turn, but mostly for drawing cards.
	Be sure to check whether or not the player is dead,
	because if a player is killed on his own turn, we will still call this on him
	"""
	def wrapUpTurn(self, player):
		raise NotImplementedError("Should be overwritten")

	"""
	When a player dies, this function will be called.
	Deal with handling recollection of tiles etc.
	"""
	def handlePlayerDeath(self, player):
		raise NotImplementedError("Should be overwritten")

 #Physical game flow:
 #   Human players have just a position
 #   AI Player has a hand, input by the keyboard
 #   Human player turn:
 #         Ask via keyboard what card was played
 #         Do not draw a card
 #   AI Turn:
 #         AI Prints out what card to play 
 # 		   Asks for input of what card it gets next
 # When a player dies:
 #   Human: 
 #     Don't do anything
 #   AI:
 #     Don't do anything
class TsuroPhysicalGame(TsuroGame):
	def __init__(self, players):
		super(TsuroGame, self).__init__(position)
	def wrapUpTurn(self, player):
		if player.alive():
			player.promptForCard()
	def handlePlayerDeath(self, player):
		pass
# Virtual Game flow
#	All players have a hand, position
#	Human player turn:
#		Game asks via keyboard what tile to play of the cards in their hand
#		Draw a card(ask game)
#	AI Turn:
#		Ai prints what card it plays
#		Asks game for new card 
class TsuroVirtualGame(TsuroGame):
	def __init__(self, players):
		super(TsuroGame, self).__init__(position)
		self.dragonIndex = None
	def wrapUpTurn(self, player):
		if player.alive():
			if self.tiles.count() == 0:
				if self.dragonIndex == None:
					self.dragonIndex = player.index
				else:
					return
			else:
				player.hand.append(self.tiles.pop())
	def handlePlayerDeath(self, player):
		self.tiles += player.hand
		random.shuffle(self.tiles)
		if self.dragonIndex is not None:
			index = self.dragonIndex
			#perform dragon distribution
			while True:
				targetPlayer = self.players[index]
				if self.tiles.count() == 0:
					self.dragonIndex = index
					return 
				elif targetPlayer.hand.count == 3:
					self.dragonIndex = None
					return
				else:
					targetPlayer.hand.append(self.tiles.pop())






#










def __main__():
	print "Number of human players?"
	numPlayers = int(sys.stdin.readLine())
	print "Number of AI players?"
	numAI = int(sys.stdin.readLine())





