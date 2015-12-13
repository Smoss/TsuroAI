lost_score = -10000000
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
	def play(self, card):
		pass

class HumanPlayer(TsuroPlayer):
	def __init__(self, name, position):



class AIPlayer (TsuroPlayer):
	#add bloodlust later
	def __init__(self, hand, position, game, P_id):
		super(TsuroPlayer, self).__init__(hand, position, game, P_id)
	def play(self):
		self.play(self, self.select_card())
	def select_card(self):
		return self.traverse(-(float("inf"), self.private_hand, self.hand, 5)
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
			points = 0
			if not self in self.game.transform(card).active_players:
				points = lost_score
			elif len(self.game.transform(card).active_players) == 1:
				return (lost_score * -.1, card)
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
				best = (points, card)
		return best

def gen_States(g_state, deck, curr_player):
	for card_order in itertools.permutations(g_state.active_players - 1):
		ng_state = copy.deepcopy(g_state)
		cp_pairs = [(g_state.active_players.remove(curr_player)[x]: card_order[x]) for x in range(len(card_order))]
		p_cards = []
		for card, player in card_order:
			if player in ng_state.active_players:
				ng_state = ng_state.transform(card)
				p_cards.append(card)
		yield ng_state, deck - p_cards






# location, name