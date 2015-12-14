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
		print "Transforming by placing tile %d at %s" % (tile.index, str(location))
		newBoard = copy.deepcopy(self.board)
		newBoard.placeTile(tile, location)
		if boardOnly:
			return newBoard
		else:
			newGame = self.cloneGame(copy.deepcopy(self.players), newBoard, self.tiles)
			newGame.moveAllPlayers()
			return newGame

	def playCard(self, tile, location):
		self.board = self.transform(tile, location, boardOnly=True)

	def gameOver(self):
		livingPlayerCount = len(self.activePlayers())
		return livingPlayerCount == 1 or livingPlayerCount == 0 or self.board.isFull()

	def playTurn(self, turn):
		print "it is turn %d" % turn
		currentPlayer = self.players[turn % len(self.players)]
		print "player %d who is at %s" % (currentPlayer.id, str(currentPlayer.position))

		if not currentPlayer.alive():
			print "Player %d is eliminated, skipping their turn" % currentPlayer.id
			return 1
		else:
			print "selecting a tile -----------------------------"
			selectedTile = currentPlayer.play()
			print "------------------------------"
			print "the selected tile is %d rotated %d times" % (selectedTile.index, selectedTile.rotation)
			if self.isSuicide(currentPlayer, selectedTile):
				print "this is suicide :( "
			else:
				print "this is not suicide, good move"
			self.playCard(selectedTile, currentPlayer.play_position())
			print "moving all players"
			self.moveAllPlayers()
			print "wrapping up turn"
			self.wrapUpTurn(currentPlayer)

	def isSuicide(self, player, tile):
		tileLocation = (player.position[0] + positions_adders[player.position[2]][0],
						player.position[1] + positions_adders[player.position[2]][1])
		tryBoard = self.transform(tile, tileLocation, boardOnly=True)
		testLocation = tryBoard.followPath(player.position, player.position[2])
		return not testLocation[0]

	def moveAllPlayers(self):
		for player in self.activePlayers():
			newLocation = self.board.followPath(player.position, player.position[2])
			print "player %d has moved from %s to %s" % (player.id, str(player.position), str(newLocation))
			player.position = (newLocation[1][0], newLocation[1][1], newLocation[2])
			if not newLocation[0]:
				print "Player %d has been eliminated" % player.id
				self.handlePlayerDeath(player)

	def activePlayers(self):
		return [livingPlayer for livingPlayer in self.players if livingPlayer.alive()]
	def active_players(self):
		return self.activePlayers()

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
	def cloneGame(self, players, board, tiles):
		game = TsuroPhysicalGame(players)
		game.board = board
		game.tiles = tiles
		return game
	def wrapUpTurn(self, player):
		if player.alive():
			player.askTerminalForTile()
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
	def cloneGame(self, players, board, tiles):
		game = TsuroVirtualGame(players)
		game.board = board
		game.tiles = tiles
		return game

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

	"""
	numPlayers = int(raw_input("Number of human players? >> ")) 
	humanPlayers = []
	for i in range(0, numPlayers):
		print "player %d" % i
		position = map(int, raw_input("enter start position: x y z >>").split(" "))
		hand = map(int, raw_input("enter tile numbers: >>").split(" "))
		hand = [TsuroTilesAllTiles[c] for c in hand]
		humanPlayers.append(HumanPlayer(hand, position, game, i))

	numAI = int(raw_input("Number of smart ai players? >> "))
	aiPlayers = []
	for i in range(0, numAI):
		print "player %d" % (i + numPlayers)
		position = map(int, raw_input("enter start position: x y z >>").split(" "))
		hand = map(int, raw_input("enter tile numbers: >>").split(" "))
		hand = [TsuroTilesAllTiles[c] for c in hand]
		humanPlayers.append(AIPlayer(hand, position, game, i + numPlayers))


	numRandom = int(raw_input("Number of random AI players? >> "))
	randomPlayers = []
	for i in range(0, numRandom):
		print "player %d" % (i + numPlayers + numAI)
		position = map(int, raw_input("enter start position: x y z >>").split(" "))
		hand = map(int, raw_input("enter tile numbers: >>").split(" "))
		hand = [TsuroTilesAllTiles[c] for c in hand]
		humanPlayers.append(RandomPlayer(hand, position, game, i + numPlayers + numAI))

	allPlayers = humanPlayers + aiPlayers + randomPlayers
	"""
	sAI = AIPlayer([TsuroTilesAllTiles[c] for c in [0, 16, 18]], (0, 3, 5), game, 0)
	dAI = RandomPlayer([TsuroTilesAllTiles[c] for c in [30, 31, 32]], (3, 0, 2), game, 1)
	game.players = [sAI, dAI]

	turnNumber = 0
	while not game.gameOver():
		game.playTurn(turnNumber)
		turnNumber += 1
		print "The turn is over"
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






