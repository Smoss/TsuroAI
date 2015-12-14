import itertools
import random

lost_score = -10000000
positions_adders = {0 : (-1, 0), 1 : (-1, 0), 2 : (0, 1), 3 : (0, 1), 4 : (1, 0), 5 : (1, 0), 6 : (0, -1), 7 : (0, -1)}
class TsuroPlayer:
	"""Contains the player's hand and position on the board."""
	def __init__(self, hand, position, game, P_id):
		self.position = position
		self.hand = hand
		self.private_hand = deck - self.hand
		self.game = game
		self.id = P_id
	def lost(self):
		adder = positions_adders[self.position[2]]
		return (position[0] + adder[0]) % 7 == 0 or (position[1] + adder[1]) % 7 == 0
	def draw(self):
		self.hand.append(self.game.draw())
	def play(self, card):
		pass
	def select_card(self):
		pass
	def play_position(self):
		return tuple(sum(x) for x in zip(player.position[:2], positions_adders[player.position[2]]))

class HumanPlayer(TsuroPlayer):
	def __init__(self, hand, position, game, P_id):
		super(TsuroPlayer, self).__init__(hand, position, game, P_id)
	def play(self):
		go = true
		while go:
			print "You currently have these cards in your hand " + zip(range(len(self.hand)),self.hand)
			play = input("Please enter your move in the form (card#,rotation#) no spaces:")
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
							go = not self.game.play(self, card.rotate(ticks = rot), self.play_position())
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


class AIPlayer (TsuroPlayer):
	#add bloodlust later
	def __init__(self, hand, position, game, P_id):
		super(TsuroPlayer, self).__init__(hand, position, game, P_id)
	def play(self):
		sel_card = self.select_card()
		self.game.play(self, sel_card[1].rotate(ticks = sel_card[2]), self.play_position())
		self.hand.remove(sel_card[1])
	def select_card(self):
		return self.traverse((-(float("inf"), self.hand[0], 0), self.private_hand, self.hand, 5)
	def symmetry(self, card):
		sym = 0
		for pair in card:
			for x in range(2, 8, 2):
				if ((pair[0] + x) % 8, (pair[1] + x) % 8) in card:
					sym += 1
		return sym
	def traverse(self, best, knowledge, hand, runs):
		if runs == 0:
			return best
		for card in self.hand:
			for rot in range(4):
				points = 0
				if not self in self.game.transform(card.rotate(ticks = rot), self.play_position()).active_players:
					points = lost_score
				elif len(self.game.transform(card.rotate(ticks = rot), self.play_position()).active_players) == 1:
					return (lost_score * -.1, card, rot)
				else:
					g_state = copy.deepcopy(game)
					points += (self.position[0] + self.position[1]) * 100 + self.symmetry(card) * 200 - len(state.active_players) * 300
					for state, n_knowledge in gen_States(g_state, self.private_hand):
						if not self in state.active_players:
							points = lost_score * .3
						elif len(state.active_players) == 1:
							points = lost_score * -.1
						else:
							for card in n_knowledge:
								points += .3 * self.traverse(best, n_knowledge - card, hand.append(card), runs - 1)[0]
				if points > best[0]:
					best = (points, card, rot)
		return best

class RandomPlayer(TsuroPlayer):
	def __init__(self, hand, position, game, P_id):
		super(TsuroPlayer, self).__init__(hand, position, game, P_id)
	def play(self):
		while not self.game.play(self, random.choice(card.rotate(ticks = random.randint(0,3))), self.play_position()):
			pass


def gen_States(g_state, deck, curr_player):
	for card_order.paths in itertools.permutations(g_state.active_players - 1):
		ng_state = copy.deepcopy(g_state)
		cp_pairs = [(g_state.active_players.remove(curr_player)[x]: card_order[x]) for x in range(len(card_order))]
		p_cards = []
		rotations = [[0]*(g_state.active_players - 1) + [1] * (g_state.active_players - 1) + [2] * (g_state.active_players - 1) + [3] * (g_state.active_players - 1)]
		for rot_list in itertools.permutations(g_state.active_players - 1):
			for rot, card, player in  itertools.izip(rot_list, card_order):
				if player in ng_state.active_players:
					ng_state = ng_state.transform(card.rotate(ticks = rot), player.play_position())
					p_cards.append(card)
		yield ng_state, deck - p_cards






# location, name