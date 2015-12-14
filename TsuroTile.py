tileTemplate = [" _ _ _ _  ",
				"| %d   %d |",
				"|%d     %d|",
				"|%d     %d|",
				"|_%d_ _%d_|"]

blankTileLines = [" _ _ _ _ ",
				"|       |",
				"|  \/   |",
				"|  /\   |",
				"|_ _ _ _|"]





allTilesInfo = [[(0, 1), (2, 3), (4, 5), (6, 7)],
         [(0, 7), (1, 6), (2, 3), (4, 5)],
		 [(4, 5), (6, 3), (7, 0), (1, 2)],
		 [(0, 7), (1, 2), (3, 4), (5, 6)],
		 [(0, 6), (1, 7), (2, 3), (4, 5)],

		 [(0, 1), (4, 5), (2, 7), (3, 6)],
		 [(0, 1), (4, 5), (2, 6), (3, 7)],
		 [(0, 6), (1, 2), (3, 7), (4, 5)],
		 [(2, 6), (3, 4), (5, 7), (0, 1)],		 
		 [(6, 0), (7, 5), (1, 2), (3, 4)],

		 [(4, 3), (5, 7), (6, 1), (2, 0)],
		 [(6, 1), (7, 3), (0, 2), (4, 5)],
		 [(4, 5), (6, 3), (7, 1), (0, 2)],
		 [(4, 5), (6, 2), (7, 1), (0, 3)],
		 [(4, 5), (6, 1), (7, 2), (0, 3)],

		 [(1, 2), (0, 3), (5, 6), (4, 7)],
		 [(0, 3), (1, 2), (7, 5), (6, 4)],
		 [(1, 2), (0, 4), (3, 6), (5, 7)],
		 [(2, 1), (3, 7), (4, 0), (5, 6)],
		 [(2, 3), (4, 6), (5, 0), (7, 1)],

		 [(5, 0), (4, 3), (7, 2), (1, 6)],
		 [(4, 6), (5, 0), (7, 3), (1, 2)],
		 [(6, 4), (5, 0), (7, 2), (1, 3)],
		 [(0, 5), (1, 3), (2, 6), (4, 7)],
		 [(2, 6), (3, 1), (4, 0), (5, 7)],

		 [(2, 0), (3, 1), (4, 6), (5, 7)],
		 [(0, 5), (1, 4), (2, 7), (3, 6)],
		 [(2, 6), (3, 7), (1, 4), (0, 5)],
		 [(0, 4), (1, 5), (2, 6), (3, 7)],
		 [(6, 2), (7, 4), (0, 3), (1, 5)],

		 [(6, 4), (7, 2), (5, 1), (0, 3)],
		 [(0, 2), (1, 5), (7, 3), (6, 4)],
		 [(0, 3), (1, 6), (2, 4), (5, 7)],
		 [(0, 6), (1, 3), (2, 4), (5, 7)],
		 [(0, 3), (1, 6), (2, 5), (4, 7)]]

class TsuroTile:
	def __init__(self, index, tileinfo, rotations=0, core=False):
		self.core = core
		self.index = index
		self.rotation = rotations 
		self.paths = [None] * 8
		if len(tileinfo) == 4:
			for a, b in tileinfo:
				self.paths[a] = b
				self.paths[b] = a
		elif len(tileinfo) == 8:
			self.paths = tileinfo

	def rotations(self):
		tiles = []
		for i in range(0, 4):
			tiles.append(self.rotate(ticks=i))
		return tiles

	def rotate(self, degrees=None, ticks=None):
		if degrees is None and ticks is None:
			return self
		elif ticks is None:
			ticks = degrees / 90
		pathPairs = enumerate(self.paths)
		#do the + 2 * ticks % 8 by pairs
		rotated = [None] * 8
		for index, destination in enumerate(self.paths):
			rotated[(index + (2*ticks)) % 8] = (self.paths[index] + (2 * ticks)) % 8
		return TsuroTile(self.index, rotated, rotations=ticks) 

	def equals(self, tile):
		otherPaths = tile.paths
		for i in range(0, 3):
			if self.paths == otherPaths:
				return True
			otherPaths = [(j + (i * 2)) % 8 for j in otherPaths]

	def drawTile(self):
		tileString = ""
		for lines in self.drawTileToLines():
			tileString += lines + "\n"
		return tileString

	def drawTileToLines(self):
		tileLines = []
		tileLines.append(tileTemplate[0])
		tileLines.append(tileTemplate[1] % (self.paths[0], self.paths[1]))
		tileLines.append(tileTemplate[2] % (self.paths[7], self.index, self.paths[2]))
		tileLines.append(tileTemplate[3] % (self.paths[6], self.paths[3]))
		tileLines.append(tileTemplate[4] % (self.paths[5], self.paths[4]))
		return tileLines
	def easyPrint(self):
		final = set()
		for index, destination in enumerate(self.paths):
			if index < destination:
				final.add((index, destination))
			else:
				final.add((destination, index))
		return final

allTiles = [TsuroTile(i, info) for i, info in enumerate(allTilesInfo)]

# Test Cases
def tests():
	testTileInfo = [(2, 3), (4, 6), (5, 0), (7, 1)]
	testTile = TsuroTile(0, testTileInfo)
	print "Test Tile: [(2, 3), (4, 6), (5, 0), (7, 1)]"
	print "Paths: " + str(testTile.paths)
	print "Rotating ..."
	testRots = testTile.rotations()
	for rotTile in testRots:
		print "%d, %s" % (rotTile.rotation, str(rotTile.paths))
	print "Testing printing:"
	print testTile.drawTile()

if __name__ == "__main__":
	tests()














