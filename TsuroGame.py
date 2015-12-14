import copy, sys
from TsuroBoard import *
from TsuroTile import TsuroTile
from TsuroTile import allTiles as TsuroTilesAllTiles
from TsuroPlayer import *
tileData = [[(0, 1), (2, 3), (4, 5), (6, 7)],
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
class TsuroGame(object):
	def __init__(self, players, board=None, tiles=None):
		self.players = players
		self.board = TsuroBoard() if board is None else board
		self.tiles = [TsuroTile(i, tileInfo) for i, tileInfo in enumerate(tileData)] if tiles is None else tiles

	def transform(self, tile, location, boardOnly=False):
		newBoard = copy.deepCopy(self.board)
		newBoard.placeTile(tile, location)
		if boardOnly:
			return newBoard
		else:
			return TsuroGame(self.players, newBoard, self.tiles)

	def playCard(self, tile, location):
		self.board = self.transform(tile, location)

	def gameOver(self):
		livingPlayerCount = len(filter((lambda p: p.alive()), self.players))
		return livingPlayerCount == 1 or livingPlayerCount == 0 or board.isFull()

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

	def isSuicide(self, player, tile):
		tileLocation = (player.position[0] + positions_adders[player.position[2]][0],
						player.position[1] + positions_adders[player.position[2]][1])
		tryBoard = self.transform(tile, tileLocation, boardOnly=True)
		testLocation = tryBoard.followPath(player.location)
		return not testLocation[0]

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
		TsuroGame.__init__(self, players)
	def wrapUpTurn(self, player):
		if player.alive():
			player.askTerminalForCard()
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
		TsuroGame.__init__(self, players)
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










def main():
	selection = int(raw_input("1 for virtual 2 for physical >>"))
	if selection == 1:
		game = TsuroVirtualGame(None)
	else:
		game = TsuroPhysicalGame(None)

	numPlayers = int(raw_input("Number of human players? >> ")) 
	humanPlayers = []
	for i in range(0, numPlayers):
		print "player %d" % i
		position = map(int, raw_input("enter start position: x y z >>").split(" "))
		hand = map(int, raw_input("enter tile numbers: >>").split(" "))
		hand = [TsuroTilesAllTiles[i] for i in hand]
		humanPlayers.append(HumanPlayer(hand, position, game, i))

	numAI = int(raw_input("Number of smart ai players? >> "))
	aiPlayers = []
	for i in range(0, numAI):
		print "player %d" % (i + numPlayers)
		position = map(int, raw_input("enter start position: x y z >>").split(" "))
		hand = map(int, raw_input("enter tile numbers: >>").split(" "))
		hand = [TsuroTilesAllTiles[i] for i in hand]
		humanPlayers.append(AIPlayer(hand, position, game, i + numPlayers))


	numRandom = int(raw_input("Number of random AI players? >> "))
	randomPlayers = []
	for i in range(0, numRandom):
		print "player %d" % i + numPlayers + numAI
		position = map(int, raw_input("enter start position: x y z >>").split(" "))
		hand = map(int, raw_input("enter tile numbers: >>").split(" "))
		hand = [TsuroTilesAllTiles[i] for i in hand]
		humanPlayers.append(RandomPlayer(hand, position, game, i + numPlayers + numAI))

	allPlayers = humanPlayers + aiPlayers + randomPlayers
	game.players = allPlayers

	turnNumber = 0
	while not game.gameOver():
		game.playTurn(turnNumber)
		turnNumber += 1
	print "The game is over!"
	print "Living players:\n-------------"
	for player in game.players:
		if player.alive():
			print player.id

if __name__ == "__main__":
	main()
			






	"""
		self.position = position
		self.hand = hand
		self.private_hand = deck - self.hand
		self.game = game
		self.id = P_id

	"""






