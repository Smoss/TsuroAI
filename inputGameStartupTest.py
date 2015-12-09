import sys

print "Number of human players?"
numPlayers = int(sys.stdin.readLine())
print "Number of AI players?"
numAI = int(sys.stdin.readLine())


for i in range(0, numPlayers):
	print "--- player " + str(i) + " ---"
	print "Name: "
	playerName = sys.stdin.readLine()
	

