import itertools
import random
import copy
from TsuroTile import allTiles as deck

lost_score = -1000000000
positions_adders = {0 : (-1, 0), 1 : (-1, 0), 2 : (0, 1), 3 : (0, 1), 4 : (1, 0), 5 : (1, 0), 6 : (0, -1), 7 : (0, -1)}
class TsuroPlayer(object):
	"""Contains the player's hand and position on the board."""
	def __init__(self, hand, position, game, P_id):
		self.position = position
		self.hand = hand
		self.private_hand = set(deck) - set(self.hand)
		self.game = game
		self.id = P_id
		print "TsuroPlayer created with id %d" % self.id
	def alive(self):
		return not self.lost()
	def lost(self):
		adder = positions_adders[self.position[2]]
		return ((self.position[0] + adder[0]) % 7 == 0 or (self.position[1] + adder[1]) % 7 == 0)

	def draw(self):
		self.hand.append(self.game.draw())
	def print_hand(self):
		print str([tile.index for tile in self.hand])
	def play(self, card):
		pass
	def select_card(self):
		pass
	def play_position(self):
		return tuple(sum(x) for x in zip(self.position[:2], positions_adders[self.position[2]]))

class HumanPlayer(TsuroPlayer):
	def __init__(self, hand, position, game, P_id):
		TsuroPlayer.__init__(self, hand, position, game, P_id)
	def play(self):
		go = true
		while go:
			print "You currently have these cards in your hand " + zip(range(len(self.hand)),self.hand)
			play = raw_input("Please enter your move in the form (card#,rotation#) no spaces:")
			if len(play) != 3:
				if ',' in play:
					play_l = play.split(',')
					if len(play_l) != 2:
						try:
							card = int(play_l[0])
							if card > len(self.hand):
								print "invalid card #"
								continue
							rot = int(play_l[1])
							if rot > 3:
								print "invalid rot # (0, 3)"
								continue
							go = not self.game.playCard(self, card.rotate(ticks = rot), self.play_position())
						except ValueError:
							print "You did not enter your play in the format #,#"
					else:
						print "You did not enter your play in the format #,#"
				else:
					print "You did not enter your play in the format #,#"
			else:
				print "There should be only 3 characters in your play"
			if not go:
				print "You gave a losing move when you have a non losing move"
	def askTerminalForTile(self):
		raw_input("A human is asking for a card, give it to them")



class AIPlayer (TsuroPlayer):
	#add bloodlust later
	def __init__(self, hand, position, game, P_id):
		TsuroPlayer.__init__(self, hand, position, game, P_id)
	def play(self, turn):
		print "Hand size = " + str(len(self.game.players))
		if turn / len(self.game.players) <= 1:
			randomTurn = RandomPlayer(self.hand, self.position, self.game, self.id)
			sel_card = randomTurn.play(0)
			sel_card = (0, sel_card, sel_card.rotation)
		else:
			sel_card = self.select_card()
		self.hand = [card for card in self.hand if card.index != sel_card[1].index]
		return sel_card[1].rotate(ticks = sel_card[2])
	def askTerminalForTile(self):
		card = int(raw_input("Please give me a card, -1 for no card >>"))
		if card != -1:
			print self.hand
			print card
			print deck[card]
			self.hand.append(deck[card])
			print "Domo arigato, from mr smrt roboto"
		else:
			print "I accept that there are no more cards"
	def select_card(self):
		return self.traverse((-float("inf"), self.hand[0], 0), self.private_hand, self.hand, 1, self.game)
	def symmetry(self, card):
		sym = 0
		for pip in card.paths:
			for x in range(2, 8, 2):
				if card.paths[(pip + x) % 8]  == ((card.paths[pip] + x) % 8):
					sym += 1
		return sym
	def traverse(self, best, knowledge, hand, runs, c_state):
		if runs == 0:
			return (0, None, 0)
		for card in hand:
			for rot in range(4):
				#print card.index
				points = 0
				g_state = c_state.transform(card.rotate(ticks = rot), c_state.players[self.id].play_position())

				
				if g_state.players[self.id].lost():
					print "yurp"
					points += lost_score
				elif g_state.gameOver():
					print "nope"
					return (lost_score * -.1, card, rot)
				else:
					num_N_N = g_state.board.numNeighborsAndEmpty(g_state.players[self.id].play_position())
					points += (g_state.players[self.id].play_position()[0] + g_state.players[self.id].play_position()[1]) * 100 + self.symmetry(card) * 500 - len(g_state.active_players())-1 * 300 + num_N_N[1] * 500
					for state, n_knowledge in gen_States(g_state, self.private_hand, self):
						if state.players[self.id].lost():
							print "huh"
							points += lost_score * .1
						elif len(state.active_players()) == 1:
							print "what"
							points += lost_score * -.1
						else:
							if len(n_knowledge) > 0:
								for card_2 in n_knowledge:
									points += .0003 * self.traverse(best, set(n_knowledge) - set([card, card_2]), set(hand) | set([card_2]) - set([card]), runs - 1, g_state)[0]
							else:
								points += .0003 * self.traverse(best, set(n_knowledge) - set([card]), hand, runs - 1, g_state)[0]
				if points > best[0]:
					best = (points, card, rot)
				#print points, card.index, rot
		return best

class RandomPlayer(TsuroPlayer):
	def __init__(self, hand, position, game, P_id):
		TsuroPlayer.__init__(self, hand, position, game, P_id)
	def play(self, turn):
		print "Hand size = " + str(len(self.hand))
		possiblePlays = []
		for card in self.hand:
			for rot in card.rotations():
				gs = self.game.transform(rot, self.play_position())
				if gs.players[self.id].alive():
					possiblePlays.append(rot)
		if possiblePlays:
			selectedTile = random.choice(possiblePlays)
		else:
			selectedTile = random.choice(self.hand).rotate(random.randint(0, 3)) 
		self.hand = [card for card in self.hand if card.index != selectedTile.index]
		return selectedTile



	def askTerminalForTile(self):
		card = int(raw_input("Please give me a card, -1 for no card >>"))
		if card != -1:
			print self.hand
			print card
			print deck[card]
			self.hand.append(deck[card])
			print "Domo arigato, from mr dum roboto"
		else:
			print "I accept that there are no more cards"

from montecarlo import runSim

class MonteCarloPlayer(TsuroPlayer):
	def __init__(self, hand, position, game, P_id):
		TsuroPlayer.__init__(self, hand, position, game, P_id)
	def play(self, turn):
		mcResults = runSim(self.game, self.id, 500)
		selectedTile = None
		maxVal = float("-inf")
		for tile in mcResults:
			runs, total = mcResults[tile]
			val = total / runs
			#print "Tile: %d rot=%d = (%s) = %f" % (tile.index, tile.rotation, str(mcResults[tile]), val)
			if val > maxVal:
				selectedTile = tile
				maxVal = val
		#print "Max: %d, %d, %f" % (selectedTile.index, selectedTile.rotation, maxVal)
		self.hand = [tile for tile in self.hand if tile.index != selectedTile.index]
		return selectedTile

	def askTerminalForTile(self):
		card = int(raw_input("Please give me a card, -1 for no card >>"))
		if card != -1:
			print self.hand
			print card
			print deck[card]
			self.hand.append(deck[card])
			print "Domo arigato, from mr dum roboto"
		else:
			print "I accept that there are no more cards"




def gen_States(g_state, deck, curr_player):
	for card_order in itertools.permutations(deck, len(g_state.active_players()) - 1):
		ng_state = copy.deepcopy(g_state)
		cp_pairs = [(list(set(g_state.active_players())- set([curr_player]))[x], card_order[x]) for x in range(len(card_order))]
		p_cards = []
		rotations = [[0]*(len(g_state.active_players()) - 1) + [1] * (len(g_state.active_players()) - 1) + [2] * (len(g_state.active_players()) - 1) + [3] * (len(g_state.active_players()) - 1)]
		for rot_list in itertools.permutations(rotations, len(g_state.active_players()) - 1):
			for rot, card_player in zip(rot_list, cp_pairs):
				card, player = card_player
				if player in ng_state.active_players():
					ng_state = ng_state.transform(card.rotate(ticks = rot), player.play_position())
					p_cards.append(card)
		yield ng_state, set(deck) - set(p_cards)
# location, name