pipTransitions = {0:5, 1:4, 2:7, 3:6, 4:1, 5:0, 6:3, 7:2}
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

	def isFull(self):
		emptySpaces = 0
		for i in range(1, 7):
			for j in range(1, 7):
				emptySpaces += 1 if self.board[i][j]
		if emptySpaces is 1:
			return True
		else:
			return False 

	#adjacentCards

