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

positions_adders = {0 : (-1, 0), 1 : (-1, 0), 2 : (0, 1), 3 : (0, 1), 4 : (1, 0), 5 : (1, 0), 6 : (0, -1), 7 : (0, -1)}
class TsuroGame:
	def __init__(self, players):
		self.players = players
		self.board = TsuroBoard()

class TsuroPlayer:
	"""Contains the player's hand and position on the board."""
	def __init__(self, hand, position):
		self.position = position
		self.hand = hand
		self.private_hand = deck - self.hand
	def lost(self):
		adder = positions_adders[self.position[2]]
		return (position[0] + adder[0]) % 7 == 0 or (position[1] + adder[1]) % 7 == 0
	def play(self, card):
		pass


class AIPlayer (TsuroPlayer):
	def init(self, hand, position):
		super(TsuroPlayer, self).__init__(hand, position)


class TsuroBoard:
	def __init__(self):
		self.board = [[None * 6] * 6]
	def placePiece(self, piece, location):
		self.board[location[0], location[1]] = piece
	def getPiece(self, location):
		return self.board[location[0], location[1]]
	def followPath(self, location, pip):
		




class TsuroPiece:



