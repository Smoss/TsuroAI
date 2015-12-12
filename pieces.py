# ___________
#|   0   1   |
#|7         2|
#|           |
#|6         3|
#|___5____4__|

[(0, 4), (1, 6), (2, 5), (3, 7)]
[(0, 7), (1, 6), (2, 4), (3, 5)]
[(0, 1), (2, 3), (4, 5), (6, 7)]
[(0, 5), (1, 3), (2, 6), (4, 7)]
[(0, 7), (1, 2), (3, 4), (5, 6)]
[(6, 7), (2, 3), (0, 4), (1, 4)]

[(1, 2), (0, 3), (5, 6), (4, 7)]
[(0, 4), (1, 5), (2, 6), (3, 7)]
[(0, 3), (1, 6), (2, 5), (4, 7)]
[(0, 6), (1, 7), (2, 4), (3, 5)]
[(0, 4), (1, 5), (7, 2), (6, 3)]
[(0, 7), (1, 4), (2, 6), (6, 3)]

[(0, 4), (1, 7), (2, 6), (3, 5)]
[(0, 2), (1, 7), (3, 4), (5, 6)]
[(0, 5), (1, 4), (2, 7), (3, 6)]
[(0, 3), (1, 5), (2, 4), (6, 7)]
[(0, 1), (2, 4), (3, 6), (5, 7)]
[(1, 2), (0, 4), (3, 6), (5, 7)]

[(0, 7), (1, 5), (2, 6), (3, 4)]
[(0, 2), (1, 5), (3, 4), (6, 7)]
[(0, 6), (7, 2), (1, 4), (3, 5)]
[(0, 6), (1, 7), (2, 3), (4, 5)]
[(0, 2), (1, 5), (7, 3), (6, 4)]

[(0, 6), (1, 3), (2, 4), (5, 7)]
[(0, 7), (1, 3), (2, 5), (6, 4)]
[(0, 4), (1, 2), (3, 5), (6, 7)]
[(0, 1), (2, 7), (3, 4), (4, 5)]
[(0, 1), (2, 7), (3, 5), (4, 6)]
[(0, 1), (2, 5), (3, 6), (4, 7)]

[(0, 2), (1, 4), (3, 7), (5, 6)]
[(0, 7), (1, 6), (2, 3), (4, 5)]
[(6, 7), (0, 4), (1, 3), (2, 5)]
[(0, 1), (4, 5), (2, 7), (3, 6)]
[(0, 3), (1, 6), (2, 4), (5, 7)]
[(0, 6), (1, 4), (7, 3), (2, 5)]

def gen_S1tates(g_state, deck, curr_player):
	for card_order in itertools.permutations(g_state.active_players - 1):
		ng_state = copy.deepcopy(g_state)
		cp_pairs = [(g_state.active_players.remove(curr_player)[x]: card_order[x]) for x in range(len(card_order))]
		p_cards = []
		for card, player in card_order:
			if player in ng_state.active_players:
				ng_state = ng_state.transform(card)
				p_cards.append(card)
		yield ng_state, deck - p_cards

lost_score = -10000000
positions_adders = {0 : (-1, 0), 1 : (-1, 0), 2 : (0, 1), 3 : (0, 1), 4 : (1, 0), 5 : (1, 0), 6 : (0, -1), 7 : (0, -1)}
class TsuroGame:
	def __init__(self, players):
		self.players = players
		self.board = TsuroBoard()

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
				for state, n_knowledge in gen_States(g_state, self.private_hand):
					if not self in state.active_players:
						points = lost_score * .3
					elif len(state.active_players) == 1:
						points = lost_score * -.1
					else:
						points += (self.position[0] + self.position[1]) * 100 + self.symmetry(card) * 300 - len(state.active_players) * 300
						for card in n_knowledge:
							points += .3 * self.traverse(best, n_knowledge - card, hand.append(card), runs - 1)[0]
			if points > best[0]:
				best = (points, card)
		return best




pipTransitions = {0:5, 1:4, 2:7, 3:6, 4:1, 5:0, 6:3, 7:2}
class TsuroGame:
	def __init__(self, players):
		self.players = players
		self.board = TsuroBoard()
		self.tiles = [TsuroTile(tileInfo) for tileInfo in tiledata]
	#transform plays a card
	#play actually plays

class TsuroBoard:
	def __init__(self):
		self.board = [[None * 8] * 8]
	
	def placeTile(self, tile, location):
		if self.isOutsidePosition(location):
			return -1
		self.board[location[0], location[1]] = tile
		return 0

	def getTile(self, location): 
		return self.board[location[0], location[1]]
	
	def followPath(self, location, pip):
		currentLocation = location
		currentPip = pip
		while True:
			nextTileLocation = (currentLocation[0] + adder[currentPip][0], currentLocation[1] + adder[currentPip][1])
			nextTilePip = pipTransitions[currentPip]
			nextTile = self.getTile(nextLocation)
			if self.isOutsidePosition(nextLocation):
				return -1
			elif nextTile is None:
				return (currentLocation, currentPip)
			else:
				currentLocation = nextTileLocation
				currentPip = nextTile.followPath(nextTilePip)

	def isOutsidePosition(self, location):
		return location[0] % 7 == 0 or
			   location[1] % 7 == 0

	#adjacentCards

class TsuroTile:
	def __init__(self, tileinfo):
		self.