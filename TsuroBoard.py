from TsuroTile import TsuroTile, blankTileLines
pipTransitions = {0:5, 1:4, 2:7, 3:6, 4:1, 5:0, 6:3, 7:2}
position_adders = {0 : (-1, 0), 1 : (-1, 0), 2 : (0, 1), 3 : (0, 1), 4 : (1, 0), 5 : (1, 0), 6 : (0, -1), 7 : (0, -1)}
startPositions = [(0, 1, 4), (0, 1, 5), (0, 2, 4), (0, 2, 5), (0, 3, 4), (0, 3, 5), (0, 4, 4), (0, 4, 5), (0, 5, 4), (0, 5, 5), (0, 6, 4), (0, 6, 5),
				(7, 1, 0), (7, 1, 1), (7, 2, 0), (7, 2, 1), (7, 3, 0), (7, 3, 1), (7, 4, 0), (7, 4, 1), (7, 5, 0), (7, 5, 1), (7, 6, 0), (7, 6, 1),
				(1, 0, 2), (1, 0, 3), (2, 0, 2), (2, 0, 3), (3, 0, 2), (3, 0, 3), (4, 0, 2), (4, 0, 3), (5, 0, 2), (5, 0, 3), (6, 0, 2), (6, 0, 3),
				(1, 7, 6), (1, 7, 7), (2, 7, 6), (2, 7, 7), (3, 7, 6), (3, 7, 7), (4, 7, 6), (4, 7, 7), (5, 7, 6), (5, 7, 7), (6, 7, 6), (6, 7, 7)]


class TsuroBoard:
	def __init__(self):
		self.board = [[None for _ in range(0, 8)] for __ in range(0,8)]  
		for i in range(0, 8):
			for j in range(0, 8):
				if (i % 7 == 0) or (j % 7 == 0):
					#print "i = %d, m7 = %d, j = %d, m7 = %d" % (i, i%7, j, j%7)
					self.board[i][j] = -1

	def placeTile(self, tile, location):
		if self.isOutsidePosition(location):
			return -1
		self.board[location[0]][location[1]] = tile
		return 0

	def getTile(self, location): 
		return self.board[location[0]][location[1]]
	
	def followPath(self, location, pip):
		currentLocation = location
		currentPip = pip
		while True:
			nextTileLocation = (currentLocation[0] + position_adders[currentPip][0], currentLocation[1] + position_adders[currentPip][1])
			nextTilePip = pipTransitions[currentPip]
			nextTile = self.getTile(nextTileLocation)
			if self.isOutsidePosition(nextTileLocation):
				return (False, currentLocation, currentPip)
			elif nextTile is None:
				return (True, currentLocation, currentPip)
			else:
				currentLocation = nextTileLocation
				currentPip = nextTile.paths[nextTilePip]

	def isOutsidePosition(self, location):
		return location[0] % 7 == 0 or \
			   location[1] % 7 == 0

	def isFull(self):
		emptySpaces = 0
		for i in range(1, 7):
			for j in range(1, 7):
				emptySpaces += 1 if not self.board[i][j] else 0
		if emptySpaces == 1:
			return True
		else:
			return False
	def printBoard(self):
		for renderRow in range(1, 7):
			rowLines = []
			for renderCol in range(1, 7):
				tile = self.board[renderRow][renderCol]
				if tile is None:
					rowLines.append(blankTileLines)
				else:
					rowLines.append(tile.drawTileToLines())
			for printLineNumber in range(0, 5):
				printingLine = ""
				for printTile in range(0, 6):
					printingLine += rowLines[printTile][printLineNumber]
				print printingLine
	def numNeighborsAndEmpty(self, position):
		cards = 0
		empty = 0
		for i in [-1, 0, 1]:
			for j in [-1, 0, 1]:
				if (i, j) == (0, 0):
					continue
				tile = self.getTile((position[0] + i, position[1] + j))
				if tile is None:
					empty += 1
				elif tile != -1:
					cards += 1
		return (cards, empty)


def tests():
	testTileData=[[(1, 2), (0, 3), (5, 6), (4, 7)],
		 [(0, 3), (1, 2), (7, 5), (6, 4)],
		 [(1, 2), (0, 4), (3, 6), (5, 7)],
		 [(2, 1), (3, 7), (4, 0), (5, 6)],
		 [(2, 3), (4, 6), (5, 0), (7, 1)],
				]
	testTiles = [TsuroTile(index, data) for index, data in enumerate(testTileData)]
	testLocations = [(1, 1), (1, 2), (2, 2), (2, 3), (2, 4), (2, 5)]
	board1 = TsuroBoard()
	print "--- Blank board ---"
	board1.printBoard()
	for tile, location in zip(testTiles, testLocations):
		print "placing tile %s at %s" % (str(tile.easyPrint()), str(location))
		board1.placeTile(tile, location)
	board1.printBoard()
	print board1.followPath((0, 1), 5)
	for i in range(1, 7):
		for j in range(1, 7):
			print "Position: (%d, %d)" % (i, j)
			print "Neighbors: %d, empty: %d" % board1.numNeighborsAndEmpty((i, j))

if __name__ == "__main__":
	tests()


	#adjacentCards

