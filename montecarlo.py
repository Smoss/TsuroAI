from TsuroTile import generateFullTiles
import random, copy, sys

def runSim(game, pid, repeats, verbose=False):
	baseGame = game
	playerId = pid
	currentPlayerId = pid

	playerIndices = [tile.index for tile in game.players[pid].hand]
	boardTiles = []
	for i in range(1, 7):
		for j in range(1, 7):
			gridTile = game.board.getTile((i, j))
			if gridTile is not None:
				boardTiles.append(gridTile.index)
	unseen = [unseenTile for unseenTile in generateFullTiles() if (unseenTile.index not in boardTiles) 
																   and (unseenTile.index not in playerIndices)]
	if verbose:
		print "boardTiles:"
		print boardTiles
		print "player indices"
		print playerIndices
		print "unseen: "
		print [tile.index for tile in unseen]

	random.shuffle(unseen)

	tileRotationsLists = [tile.rotations() for tile in game.players[pid].hand] 
	possibleMoves = []
	backupMove = None
	for tileRotationList in tileRotationsLists:
		for rot in tileRotationList:
			backupMove = rot
			if not game.isSuicide(game.players[pid], rot):
				possibleMoves.append(rot)
	#print possibleMoves
	if not possibleMoves:
		print "no possible moves"
		return {backupMove : (0, 0)}
	results = {possibleMove: (0, 0) for possibleMove in possibleMoves}


	if verbose:
		print "Running %d games" % repeats

	repeatsPerTick = repeats/20
	nextTarget = repeatsPerTick
	for run in range(0, repeats):
		random.shuffle(unseen)
		chosenMove = random.choice(possibleMoves)
		if verbose:
			print "Running game %d starting with tile %d rot %d" % (run, chosenMove.index, chosenMove)
		elif run >= nextTarget:
			sys.stdout.write(".")
			nextTarget += repeatsPerTick

		chosenTransformation = baseGame.transform(chosenMove, game.players[pid].play_position())
		chosenTransformation.players[pid].hand = [tile for tile in chosenTransformation.players[pid].hand if tile.index != chosenMove.index]
		result = runFullGame(chosenTransformation, 
							  pid,
							 (pid + 1) % len(game.players),
							 copy.deepcopy(unseen))
		results[chosenMove] = (results[chosenMove][0] + 1, results[chosenMove][0] + result)
	if not verbose:
		print ""
	return results

def runFullGame(gameState, playerPid, currentPid, unseen):
	value = 0
	while not gameState.players[playerPid].lost():
		activePlayers = len(gameState.activePlayers())
		if len(unseen) == 0 or gameState.gameOver():
			#print "i won"
			return 200
		currentPlayer = gameState.players[currentPid]
		invalids = []
		validRots = []
		if playerPid != currentPid:
			while len(unseen) > 0 and len(validRots) == 0:
				randomTile = unseen.pop()
				validRots = [rot for rot in randomTile.rotations() if not gameState.isSuicide(currentPlayer, rot)]
				if not validRots:
					invalids.append(randomTile)
			
			if validRots:
				selection = random.choice(validRots)

			elif invalids:
				selection = random.choice(invalids)
				unseen.extend([invalid for invalid in invalids if invalid.index != selection.index])
		else:
			if(len(currentPlayer.hand) != 0):
				random.shuffle(currentPlayer.hand)
				handSelection = None
				for randomPlayerHandSelection in currentPlayer.hand:
					tileRots = randomPlayerHandSelection.rotations()
					validRots = [validRot for validRot in tileRots if not gameState.isSuicide(currentPlayer, rot)]
					if validRots:
						handSelection = random.choice(validRots)
						break
				if handSelection is None:
					while len(unseen) > 0 and len(validRots) == 0:
						randomTile = unseen.pop()
						validRots = [rot for rot in randomTile.rotations() if not gameState.isSuicide(currentPlayer, rot)]
						if not validRots:
							invalids.append(randomTile)

					if validRots:
						selection = random.choice(validRots)

					elif invalids:
						selection = random.choice(invalids)
						unseen.extend([invalid for invalid in invalids if invalid.index != selection.index])
				else:
					currentPlayer.hand = [card for card in currentPlayer.hand if card.index != handSelection.index]
					selection = handSelection
			else:
				while len(unseen) > 0 and len(validRots) == 0:
						randomTile = unseen.pop()
						validRots = [rot for rot in randomTile.rotations() if not gameState.isSuicide(currentPlayer, rot)]
						if not validRots:
							invalids.append(randomTile)

				if validRots:
					selection = random.choice(validRots)

				elif invalids:
					selection = random.choice(invalids)
					unseen.extend([invalid for invalid in invalids if invalid.index != selection.index])


		gameState = gameState.transform(selection, currentPlayer.play_position())

		if playerPid == currentPid:
			if activePlayers > len(gameState.activePlayers()) and not gameState.players[playerPid].lost():
				value += 100
				#print "i killed a guy"
			else:
				value += 1
		else:
			value += 1

		currentPid = (currentPid + 1) % len(gameState.players)

	return value













