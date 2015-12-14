import itertools
import random
import copy
from TsuroTile import allTiles as deck

lost_score = -10000000
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
	def play(self):
		sel_card = self.select_card()
		return sel_card[1].rotate(ticks = sel_card[2])
	def askTerminalForTile(self):
		card = int(raw_input("Please give me a card, -1 for no card"))
		if card != -1:
			self.hand += TsuroTile.allTiles[card]
			print "Domo arigato, from mr smrt roboto"
		print "I accept that there are no more cards"
	def select_card(self):
		return self.traverse((-float("inf"), self.hand[0], 0), self.private_hand, self.hand, 5)
	def symmetry(self, card):
		sym = 0
		for pip in card.paths:
			for x in range(2, 8, 2):
				if card.paths[(pip + x) % 8]  == ((card.paths[pip] + x) % 8):
					sym += 1
		return sym
	def traverse(self, best, knowledge, hand, runs):
		if runs == 0:
			return best
		for card in self.hand:
			for rot in range(4):
				points = 0
				g_state = self.game.transform(card.rotate(ticks = rot), self.play_position())
				
				print "gstate info:"
				print g_state.players
				g_state.board.printBoard()

				if g_state.players[self.id].lost():
					points = lost_score
				elif g_state.gameOver():
					return (lost_score * -.1, card, rot)
				else:
					num_N_N = g_state.board.numNeighborsAndEmpty(g_state.players[self.id].play_position())
					points += (g_state.players[self.id].position[0] + g_state.players[self.id].position[1]) * 100 + self.symmetry(card) * 50 - len(g_state.active_players())-1 * 300 + num_N_N[1] * 500
					for state, n_knowledge in gen_States(g_state, self.private_hand, self):
						if not self in state.active_players():
							points += lost_score * .3
						elif len(state.active_players()) == 1:
							points += lost_score * -.1
						else:
							if len(n_knowledge) > 0:
								for card in n_knowledge:
									points += .3 * self.traverse(best, set(n_knowledge) - set([card]), hand.append(card), runs - 1)[0]
							else:
								points += .3 * self.traverse(best, set(n_knowledge) - set([card]), hand, runs - 1)[0]
				if points > best[0]:
					best = (points, card, rot)
		return best

class RandomPlayer(TsuroPlayer):
	def __init__(self, hand, position, game, P_id):
		TsuroPlayer.__init__(self, hand, position, game, P_id)
	def play(self):
		card = random.choice(card.rotate(ticks = random.randint(0,3)))
		while self.game.isSuicide(self, card):
			card = random.choice(card.rotate(ticks = random.randint(0,3)))
		return card11
	def askTerminalForTile(self):
		card = int(raw_input("Please give me a card, -1 for no card"))
		if card != -1:
			self.hand += TsuroTile.allTiles[card]
			print "Domo arigato, from mr dum roboto"
		print "I accept that there are no more cards"


def gen_States(g_state, deck, curr_player):
	for card_order in itertools.permutations(deck, len(g_state.active_players()) - 1):
		ng_state = copy.deepcopy(g_state)
		cp_pairs = [(list(set(g_state.active_players())- set([curr_player]))[x], card_order[x]) for x in range(len(card_order))]
		p_cards = []
		rotations = [[0]*(len(g_state.active_players()) - 1) + [1] * (len(g_state.active_players()) - 1) + [2] * (len(g_state.active_players()) - 1) + [3] * (len(g_state.active_players()) - 1)]
		for rot_list in itertools.permutations(rotations, len(g_state.active_players()) - 1):
			for rot, card_player in zip(rot_list, card_order):
				print "card_player"
				print card_player
				card, player = card_player
				if player in ng_state.active_players():
					ng_state = ng_state.transform(card.rotate(ticks = rot), player.play_position())
					p_cards.append(card)
		yield ng_state, deck - p_cards
# location, name