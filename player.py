import sys

class Player:

	def __init__ (self, colour):
		self.colour = colour
		self.board = Board()
		self.pieces = getPieces() #not sure if this is that useful but chucked her in anyway
		self.exits = getExits(colour)

	def action(self):
		#TODO: write the code here for our actual parts of the program
		pieceSet = pieces
		depth = 2 #looking 2 moves ahead

		possibleMoves = getPossibleMoves(pieceSet) #get initial node and neighbour set from the first state
		start = myNode(pieceSet, None)

		generateTree(node, allmoves, 0, depth) #start node should now be a whole tree

		#get ideal move. move is key in dictionary, maybe we can get from there?
		moves = list(start.neighbours.keys())

		for node in start.neighbours:
			if node.value == start.value: #then this is the move we want
				bestMove = start.neighbours.key(node)
		
		return bestMove

	#recursively generates a tree of move states up until n depth (i think this function is very clever and i am v proud of it :^)  )
	def generateTree(node, pieceSet, current, depth):

		if current == depth:
			#here we can change it to run a reverse eval function/minimax on the tree
			return

		possibleMoves = getPossibleMoves(pieceSet) #we have a set of possible moves
		possibleNodes = {}

		best = 100000000000

		for move in possibleMoves:
			#TODO: might create some funky logic where we get a set of pieces with no moves, i guess this is okay though? 
			#THEORY: might create a bunch of irrelevant possible move nodes
			newNode = myNode(getPiecesFromMove(move,pieceSet), {}) #generate a new node for each 
			tempScore = calculateScore(newNode.peeces)
			newNode.value = tempScore
			newNode.neighbours = generateTree(newNode,newNode.peeces,current+1,depth) #recursive here, 
			possibleNodes[move] = newNode #generates as we minimax?
			if tempScore < best: #THEORY: should work recursively upwards: each recursion gets the best from it's children
				best = tempScore
			#can do a score metric in here that keeps track of the lowest distance out of the nieghbours and sets the parent value to be this

		node.neighbours = possibleNodes
		node.value = best

		return None
		
	def update(self, colour, action):
		self.board.update(colour, action)

	def getPieces(): #helper function to return current pieces
		pizzi = []
		for piece in board.pieces:
			if piece.colour == colour:
				pizzi.append(piece)
		return pizzi

	def getPossibleMoves(pieceSet):
		moves = []
		#for all pieces, find all neighbours
		for piece in pieceSet:
			moves.append(piece.getPossibleMoves(board, pieceSet))

		#now we have ALL possible moves we can make from the current position
		return moves

	def calculateScore(reeces):
		score = 0
		
		for peeces in reeces:
			best = 10000
			for exit in exits:
				temp = heuristic(peeces, exit)	
				if temp < best:
					temp = best

			score += best #add the shortest cost to any exit to the score
		
		return score
	
	def getPiecesFromMove(move, currentPieces):
		bigBoy = []

		for peeze in currentPieces:
			if peeze in move:
				if(move[2]!=(69,69)): #distance will be 0 if we are on an exit so no need to add it
					bigBoy.append(move[2]) #add the new location as if we had moved
			else:
				bigBoy.append(peeze)
		
		return bigBoy

	def heuristic(tup, exit):
		(x1, y1) = tup
    	(x2, y2) = exit
    	return ((abs(x1-x2) + abs(x1 + y1 - x2 - y2) + abs(y1-y2))/2)

	def getExits(colour):
		if colour == 'R':
			return [(3,-3),(3,-2),(3,-1),(3,0)]
		elif colour == 'B':
			return [(-3,3),(-2,3),(-1,3),(0,3)]
		elif colour == 'G':
			return [(-3,0),(-3,1),(-3,2),(-3,3)]