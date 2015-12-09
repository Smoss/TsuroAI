





def rotate(piece, rotation):
	rot = rotation / 90
	rotated = []
	l = lambda x : (x + (rot * 2)) % 8
	for a, b in piece:
		rotated.append((l(a), l(b)))
	return rotated

inputPiece = [(0, 5), (1, 7), (2, 3), (4, 6)]
for i in range(0, 5):
	print "rotating clockwise %d times" % i
	print rotate(inputPiece, i * 90)