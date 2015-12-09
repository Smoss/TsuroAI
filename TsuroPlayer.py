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

class HumanPlayer(TsuroPlayer):
	def __init__(self, name, position):



class AIPlayer (TsuroPlayer):
	def init(self, hand, position):
		super(TsuroPlayer, self).__init__(hand, position)






# location, name