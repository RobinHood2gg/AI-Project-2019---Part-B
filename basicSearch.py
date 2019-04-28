import sys

class BasicSearch:

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

		return node

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

    def heuristic(tup, exit):
		(x1, y1) = tup
    	(x2, y2) = exit
    	return ((abs(x1-x2) + abs(x1 + y1 - x2 - y2) + abs(y1-y2))/2)