from TsuroTile import generateFullTiles
import random, copy, sys
import numpy as np
from scipy import stats
from itertools import product
import time
def monteCarloMod1(state, pid, knowledge):
	random.seed()
	b_state = copy.deepcopy(state)
	p_id = pid
	c_id = pid
	cards_0 = b_state.players[pid].hand
	cards = []
	print "pid is" , pid
	for card in cards_0:
		for rot in range(4):
			if not state.transform(card.rotate(ticks=rot), state.players[pid].play_position()).players[pid].lost():
				cards.append((card, rot))
	if not cards:
		return random.choice(cards_0), random.randint(0, 3)
	return tourney(b_state, cards, pid, knowledge)

def tourney(state, cards, pid, knowledge):
	if len(cards) == 1:
		print "playing", cards[0][0].index, cards[0][1]
		return cards[0][0], cards[0][1]
	r_p_card = (120*32)/(len(cards)*len(knowledge)+1)
	v_dict = {}
	v_array = []
	c_time = time.clock()
	for card, rot in cards:
		wins = []
		for sim_n in range(r_p_card):
			if runSimMod1(copy.deepcopy(state), pid, card.rotate(ticks = rot), list(set(state.players[pid].hand) - set([card])), knowledge):
				wins.append(1)
			else:
				wins.append(0)
		v_array.extend(wins)
		wins = np.array(wins)
		v_dict[card.rotate(ticks = rot)] = (wins, card, rot)
	v_array = np.array(v_array)
	next_round = []
	mean = np.sum(v_array)/np.int_(len(cards))
	for wins, card, rot in v_dict.values():
		print card.index, rot, ":", np.sum(wins), mean, r_p_card
		if np.sum(wins) > mean:
			next_round.append((card,rot))
	if len(next_round) == 0:
		return tourney(state, [random.choice(cards)], pid, knowledge)
	print "New Round with " + str(len(next_round))
	return tourney(state, next_round, pid, knowledge)

def runSimMod1(state, pid, c_card, hand, knowledge):
	state = state.transform(c_card, state.players[pid].play_position())
	cid = pid
	num_players = len(state.players)
	deck = list(copy.deepcopy(knowledge))
	random.shuffle(deck)
	while not state.players[pid].lost():
		cid = incrementPlayer(cid, num_players)
		if state.gameOver():
			return True
		while state.players[cid].lost():
			cid = incrementPlayer(cid, num_players)
		c_play_position = state.players[cid].play_position()
		if cid == pid:
			p_cards = [x for x in product(range(len(hand)), range(4))]
			random.shuffle(p_cards)
			cont = False
			for card in p_cards:
				n_state = state.transform(hand[card[0]].rotate(ticks = card[1]), c_play_position)
				if not n_state.players[pid].lost():
					hand.remove(hand[card[0]])
					state = n_state
					cont = True
					break
			if cont:
				continue
		if not deck:
			return False
		allow_i_suicide = num_players >= len(deck)
		state = pick_card(deck, allow_i_suicide, c_play_position, cid, state)
	return False

def incrementPlayer(curr, num_players):
	return (curr + 1) % num_players

def pick_card(deck, can_die, c_play_position, cid, state):
	for card in deck:
		rots = range(4)
		random.shuffle(rots)
		for rot in rots:
			n_state = state.transform(card.rotate(ticks = rot), c_play_position)
			if not n_state.players[cid].lost():
				deck.remove(card)
				return n_state
		if can_die:
			n_state = state.transform(card.rotate(ticks = rot), c_play_position)
			deck.remove(card)
			return n_state
	state = state.transform(deck.pop(0).rotate(ticks=random.randint(0,3)), c_play_position)
	return state

"""
Run a simulation starting from game gamestate for player id pid for repeat simulations
"""
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













