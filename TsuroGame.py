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
		#print "Transforming by placing tile %d at %s" % (tile.index, str(location))
		newBoard = copy.deepcopy(self.board)
		newBoard.placeTile(tile, location)
		if boardOnly:
			return newBoard
		else:
			newGame = self.cloneGame(copy.deepcopy(self.players), newBoard, copy.deepcopy(self.tiles))
			newGame.moveAllPlayers()
			return newGame

	def playCard(self, tile, location):
		self.board = self.transform(tile, location, boardOnly=True)

	def gameOver(self):
		livingPlayerCount = len(self.activePlayers())
		#print "there are %d living players out of %d total" % (livingPlayerCount, len(self.players))
		return livingPlayerCount == 1 or livingPlayerCount == 0 or self.board.isFull()

	def playTurn(self, turn):
		print "--------------------------------------------------------"
		print "it is turn %d" % turn
		for player in self.players:
			print "%d: %s" % (player.id, (str([tile.index for tile in player.hand])) if player.alive() else "DEAD")
		print "--------------------------------------------------------"
		currentPlayer = self.players[turn % len(self.players)]
		print "player %d who is at %s" % (currentPlayer.id, str(currentPlayer.position))

		if not currentPlayer.alive():
			print "Player %d is eliminated, skipping their turn" % currentPlayer.id
			return 1
		else:
			print "Their hand:"
			print currentPlayer.print_hand()
			print "selecting a tile \n-----------------------------"
			selectedTile = currentPlayer.play(turn)
			print "------------------------------"
			print "the selected tile is %d rotated %d times" % (selectedTile.index, selectedTile.rotation)
			#print "the base card paths are %s" % TsuroTilesAllTiles[selectedTile.index].easyPrint()
			#print "The rotated paths are: %s" % selectedTile.easyPrint()
			if self.isSuicide(currentPlayer, selectedTile):
				print "this is suicide :( "
			else:
				print "this is not suicide, good move"
			self.playCard(selectedTile, currentPlayer.play_position())
			self.board.printBoard()
			print "moving all players"
			self.moveAllPlayers(report=True)
			print "wrapping up turn"
			self.wrapUpTurn(currentPlayer)
			print "--------------------------------------------------------------"
			#raw_input("<>")
	def printDeck(self):
		print "Deck remaining: %d cards" % len(self.tiles)
		print str([tile.index for tile in self.tiles])


	def isSuicide(self, player, tile):
		tileLocation = (player.position[0] + positions_adders[player.position[2]][0],
						player.position[1] + positions_adders[player.position[2]][1])
		tryBoard = self.transform(tile, tileLocation, boardOnly=True)
		testLocation = tryBoard.followPath(player.position, player.position[2])
		return not testLocation[0]

	def moveAllPlayers(self, report=False):
		for player in self.activePlayers():
			newLocation = self.board.followPath(player.position, player.position[2])
			if report:
				print "player %d has moved from %s to %s" % (player.id, str(player.position), str(newLocation))
			player.position = (newLocation[1][0], newLocation[1][1], newLocation[2])
			if not newLocation[0]:
				if report:
					print "Player %d has been eliminated" % player.id
				self.handlePlayerDeath(player, report)

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
		game.dragonIndex = self.dragonIndex
		return game
	def dealInitalTiles(self):
		print "Dealing initial tiles"
		random.shuffle(self.tiles)
		for i in range(0, 3):
			print "deaing everyone card %d" % (i + 1)
			for player in self.players:
				player.hand.append(self.tiles.pop())

	def wrapUpTurn(self, player, verbose=False):
		print "Attempting to resolve dragon tile"
		if self.dragonIndex is not None and not self.gameOver():
			print "the dragon tile starts on character %d" % self.dragonIndex
			index = self.dragonIndex
			#perform dragon distribution
			while True:
				print "current dragon index %d" % index
				targetPlayer = self.players[index]
				if len(self.tiles) == 0:
					print "there are no tiles to dispense, leaving dragon index on %d" % index
					self.dragonIndex = index
					break
				elif len(targetPlayer.hand) == 3:
					print "the person with the index has a hand of three, the dragon again slumbers"
					self.dragonIndex = None
					break
				elif targetPlayer.lost():
					print "player %d is out, skipping" % index
				else:
					dTile = self.tiles.pop()
					print "dispensing tile %d to player %d" % (dTile.index, index)
					targetPlayer.hand.append(dTile)
				index = (index + 1) % len(self.players)
		elif verbose:
			print "No dragon tile had been given"

		print "Wrapping up turn for player " + str(player.id)
		if player.alive():
			print "The player is still alive"
			if len(self.tiles) == 0:
				print "The deck is empty"
				if self.dragonIndex == None:
					print "Setting dragon tile to %d" % player.id
					self.dragonIndex = player.id
				else:
					print "dragon tile has already been set as %d" % self.dragonIndex
					return
			else:
				print "the deck is not empty"
				tile = self.tiles.pop()
				print "giving player %d card %d" % (player.id, tile.index)
				player.hand.append(tile)
				self.printDeck()
	def handlePlayerDeath(self, player, verbose=False):
		if verbose:
			print "XXXXXXXXXXXXXXXXXXXXXXXXXX"
			print "Handling the death of player %d" % player.id
			print "deck before upkeep"
			self.printDeck()
		self.tiles += player.hand
		player.hand = []
		if verbose:
			print "deck after upkeep"
			self.printDeck()
		random.shuffle(self.tiles)
		if verbose:
			print "deck after upkeep and shuffle"
			self.printDeck()
			print "XXXXXXXXXXXXXXXXXXXXXXXXXX"







#










def main():
	selection = int(raw_input("1 for virtual 2 for physical >>"))
	if selection == 1:
		game = TsuroVirtualGame(None)
		virtualGame = True
	else:
		virtualGame = False
		game = TsuroPhysicalGame(None)

	random.shuffle(startPositions)

	numPlayers = int(raw_input("Number of human players? >> ")) 
	humanPlayers = []
	for i in range(0, numPlayers):
		print "player %d" % i
		position = map(int, raw_input("enter start position: x y z >>").split(" "))
		if virtualGame:
			hand = []
		else:
			hand = map(int, raw_input("enter tile numbers: >>").split(" "))
			hand = [TsuroTilesAllTiles[c] for c in hand]
		humanPlayers.append(HumanPlayer(hand, position, game, i))



	numAI = int(raw_input("Number of smart ai players? >> "))
	aiPlayers = []
	for i in range(0, numAI):
		print "player %d" % (i + numPlayers)
		position = raw_input("enter start position: x y z -1 for random>>")
		if position == "-1":
			position = startPositions.pop()
			print "randomly chose %s" % str(position)
		else:
			position = map(int, position.split(" "))

		if virtualGame:
			hand = []
		else:
			hand = map(int, raw_input("enter tile numbers: >>").split(" "))
			hand = [TsuroTilesAllTiles[c] for c in hand]		
		aiPlayers.append(AIPlayer(hand, position, game, i + numPlayers))

	numMC = int(raw_input("Number of monte players? >> "))
	mcPlayers = []
	for i in range(0, numMC):
		print "player %d" % (i + numPlayers + numAI)
		position = raw_input("enter start position: x y z -1 for random>>")
		if position == "-1":
			position = startPositions.pop()
			print "randomly chose %s" % str(position)
		else:
			position = map(int, position.split(" "))

		if virtualGame:
			hand = []
		else:
			hand = map(int, raw_input("enter tile numbers: >>").split(" "))
			hand = [TsuroTilesAllTiles[c] for c in hand]		
		mcPlayers.append(MonteCarloPlayer(hand, position, game, i + numPlayers + numAI))


	numRandom = int(raw_input("Number of random AI players? >> "))
	randomPlayers = []
	for i in range(0, numRandom):
		print "player %d" % (i + numPlayers + numAI + numMC)
		position = raw_input("enter start position: x y z -1 for random>>")
		if position == "-1":
			position = startPositions.pop()
			print "randomly chose %s" % str(position)
		else:
			position = map(int, position.split(" "))
		if virtualGame:
			hand = []
		else:
			hand = map(int, raw_input("enter tile numbers: >>").split(" "))
			hand = [TsuroTilesAllTiles[c] for c in hand]		
		randomPlayers.append(RandomPlayer(hand, position, game, i + numPlayers + numAI + numMC))

	allPlayers = humanPlayers + aiPlayers + mcPlayers + randomPlayers 
	print humanPlayers
	print aiPlayers
	print mcPlayers
	print randomPlayers
	print allPlayers
	game.players = allPlayers

	if virtualGame:
		game.dealInitalTiles()
	turnNumber = 0
	print "-------------pregame---------------"
	game.printDeck()



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






