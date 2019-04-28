import sys
import importlib

class Player:

	def __init__ (self, colour):
        board = input('basicSearch.py')
        piece = input('piece.py')
        node = input('myNode.py')
        importlib.import_module(board)
        importlib.import_module(piece)
        importlib.import_module(node)

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

		for node in start.neighbours:
			if node.value == start.value: #then this is the move we want
				bestMove = start.neighbours.key(node)
		
		return bestMove
		
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
	
	def getPiecesFromMove(move, currentPieces):
		bigBoy = []

		for peeze in currentPieces:
			if peeze in move:
				if(move[2]!=(69,69)): #distance will be 0 if we are on an exit so no need to add it
					bigBoy.append(move[2]) #add the new location as if we had moved
			else:
				bigBoy.append(peeze)
		
		return bigBoy

	def getExits(colour):
		if colour == 'R':
			return [(3,-3),(3,-2),(3,-1),(3,0)]
		elif colour == 'B':
			return [(-3,3),(-2,3),(-1,3),(0,3)]
		elif colour == 'G':
			return [(-3,0),(-3,1),(-3,2),(-3,3)]