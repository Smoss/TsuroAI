class TsuroTile:
	def __init__(self, index, tileinfo, rotations=0, core=False):
		self.core = core
		self.index = index
		self.rotation = rotations 
		self.paths = [None * 8]
		if len(tileinfo) == 4:
			for a, b in tileinfo:
				self.paths[a] = b
				self.paths[b] = a
		elif len(tileinfo) == 8:
			self.paths = tileinfo

	def rotations(self):
		tiles = []
		for i in range(0, 4):
			tiles.append(self.rotate(i * 90))
		return tiles

	def rotate(self, ticks):
		rotated = [None * 8]
		for i in len(self.paths):
			rotated[i] = (self.paths[i] + (2 * ticks)) % 8
		return TsuroTile(parsed=self.index, rotated, rotations=ticks) 

	def equals(self, tile):
		otherPaths = tile.paths
		for i in range(0, 3):
			if self.paths == otherPaths:
				return True
			otherPaths = [(j + (i * 2)) % 8 for j in otherPaths]


