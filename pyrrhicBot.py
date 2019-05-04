import sys
import json
from queue import PriorityQueue

class myNode:

	#each node will represent a state, with it's neighbours being the states it can get to represented by all possible moves
	#will only generate the board state for each when it is explored to save computational power
	#maybe dont assign em to a priority queue but have a graph structure, seeing we want to explore them ALL and then reverse engineer costs

	#THEORY: do we need to generate the whole board again? probably not, I think we only need to compute the distances between the pieces and the exits
	def __init__(self, pieces):
		self.peeces = pieces 
		self.neighbours = []#neigh is a dict of move to piece states
		self.value=0 #minimax value
		self.colour = None

	def __lt__(self, other):
		return self.value < other.value

	def __eq__(self,other):
		if isinstance(other, self.__class__):
			return self.peeces == other.peeces and self.value == other.value #and self.neighbours == other.neighbours

	def __hash__(self):
		return hash((str(self.neighbours))) #assume we are in the same state if we have the same possible moves?
		#YEB: there will never be a case where this is NOT the case

	def __ne__(self, other):
		return not self.__eq__(other)


#smartBot incoming
class Player:

	def __init__ (self, colour):
		self.colour=colour
		self.board = Board()
		self.exits = getExits(colour)
		self.MAX_DEPTH = 3 #one for each player
		self.path = None

	
	def action(self):
		
		defaultMove = ("PASS", None)
		#TODO: hard code in early game strategies
		#TODO: use a* to end game once there are no enemy pieces left
		#TODO: change evaluation heuristic to calculate the ideal distance from others being a one tile seperation radius
		if self.board == None:
			return defaultMove
		if not checkPieceHasColours(self.colour,self.board.pieces):
			return defaultMove

		#TODO: program in early game formations
		if self.path != None: #No players left and we have generated path, do moves until we exit fully
			return moveToExitGivenPath(self.path)
		
		#IF THERE ARE NO PLAYERS LEFT: a* search to generate path
		elif not checkPieceHasColours(getNextColour(self.colour),self.board.pieces) and not checkPieceHasColours(getNextColour(self.colour,True),self.board.pieces):
			temp = getAllPathsToExit(self.board.pieces,self.exits)
			self.path = formatExitPathsAsMoves(temp,self.exits)
			#print(self.path)
			return moveToExitGivenPath(self.path)

		#Otherwise if one player is eliminated run a 2 player minimax algorithm
		elif not checkPieceHasColours(getNextColour(self.colour),self.board.pieces) or not checkPieceHasColours(getNextColour(self.colour,True),self.board.pieces):
			self.MAX_DEPTH = 3 #TODO: implement alpha beta pruning
			start = myNode(self.board.pieces)
			self.twoPlayerMinimax(self.colour,1,self.board.pieces,1,start)
		else:
			self.MAX_DEPTH = 4 #TODO: fix program getting confused and being other player sometimes
			start = myNode(self.board.pieces)
			self.myMinimax(self.colour,1,self.board.pieces,1,start)
		
		best = 0
		currentBest = None
		for move in start.neighbours:
			if move.value > best:
				best = move.value
				currentBest = move

		if currentBest != None:
			bestMove = getMoveFromPieces(currentBest.peeces,self.board.pieces)
		else:
			bestMove = move

		return bestMove

		#TODO: next TODO: implement alpha beta pruning

		#basic metric to pick a move that is a jump move out of all the possible moves
		#bestMove = None
		#move = None 
		#for neigh in bigDick[score]:
		#	if neigh != self.board.pieces:
		#		move = getMoveFromPieces(neigh,self.board.pieces)
		#		if "JUMP" in move:
		#			bestMove = move

		#if move == None:
		#	for num in bigDick:
		#		for mov in bigDick[num]:
		#			move = getMoveFromPieces(mov,self.board.pieces)

			#all the best scoring moves
			#there is 16 moves in here
			#do some if checking for if the move is 
			#miniMove = getMoveFromPieces(neigh,self.board.pieces)
			#print(miniMove)

		#move = getMoveFromPieces(miniMove,getPiecesOfColour(self.board.pieces,self.colour))
		#moves = generateMoves(self.board.pieces, self.colour, self.exits)

		#hell yeah - our boy isn't smart but he works!
		#if bestMove != None:
		#	return bestMove


	def update(self, colour, action):
		self.board.update(colour,action)

	def twoPlayerMinimax(self,currentColour,depth,board,signFactor,node):

		node.colour = currentColour
		if depth == 1:
			nextCol = currentColour
		else:
			nextPlayer = getNextColour(currentColour)
			nexterPlayer = getNextColour(currentColour,True)
			if checkPieceHasColours(nextPlayer,board):
				nextCol = nextPlayer
			else:
				nextCol = nexterPlayer

		if depth == self.MAX_DEPTH:
			return

		exits = getExits(currentColour)
		moves = generateMoves(board,currentColour,exits)
		
		signFactor = signFactor*(-1) #SHOULD: work

		for move in moves:
			#also here passing in next colour, 
			newBoard = generateBoardFromMove(nextCol,move,board)
			thisScore = evaluatePosition(currentColour,newBoard,move,3)
			newNode = myNode(newBoard)
			newNode.value = thisScore
			self.myMinimax(nextCol,depth+1,newBoard,signFactor,newNode)

			node.neighbours.append(newNode)
		
		return None

	def myMinimax(self,currentColour,depth,board,signFactor,node): #board is an array of the pieces with colours

		node.colour = currentColour
		if depth == 1:
			nextCol = currentColour
		else:
			nextCol = getNextColour(currentColour)
		
		if depth == self.MAX_DEPTH:
			return

		if currentColour == self.colour:
			signFactor = 1
		else:
			signFactor = -1

		exits = getExits(currentColour)
		moves = generateMoves(board,currentColour,exits)

		for move in moves:
			#also here passing in next colour, 
			newBoard = generateBoardFromMove(nextCol,move,board)
			thisScore = evaluatePosition(currentColour,newBoard,move,3)
			newNode = myNode(newBoard)
			newNode.value = thisScore
			self.myMinimax(nextCol,depth+1,newBoard,signFactor,newNode)

			node.neighbours.append(newNode)

		return None


def moveToExitGivenPath(path):
	move = path[0]
	del path[0]

	return move

def formatExitPathsAsMoves(path,exits):

	paths = []
	pathCreated = []
	#path[piece] = move
	for i in range(0,4): #pick the most efficient exit and find a path, repeat 4 times
		best = 10000000
		for piece in path:
			if len(path[piece]) < best and path[piece] not in pathCreated:
				best = len(path[piece])
				ourBoi = path[piece]

		pathCreated.append(ourBoi)

		for j in range(0,len(ourBoi)):
			if j == len(ourBoi) - 1:
				paths.append(("EXIT",ourBoi[j]))
				break
			else:
				#we dont consider jumps for the shortest path to simplify ending the game so we can assume any none-exit move is a regular move
				paths.append(("MOVE",(ourBoi[j],ourBoi[j+1])))

	return paths

def getAllPathsToExit(pieces, exits): 
	best = 10000000
	bestExst = None
	pathToTake = {}
	for pieceToExit in pieces:
		for exit in exits:
			yummy = heuristic((pieceToExit.column,pieceToExit.row),exit)
			if yummy < best:
				best = yummy
				bestExst = exit

		pathMap, costs = AStarSearch((pieceToExit.column,pieceToExit.row), bestExst)

		#now reverse engineer the path
		esrever = []
		loc = bestExst
		while loc != (pieceToExit.column,pieceToExit.row): #work backwards to get the full path traversed
			esrever.append(loc)
			loc = pathMap[loc]
		esrever.append((pieceToExit.column,pieceToExit.row))
		esrever.reverse()

		pathToTake[pieceToExit] = esrever

	return pathToTake

def AStarSearch(start, exit): 

	nodeLoad = PriorityQueue()
	nodeLoad.put(start,0)
	previousVisits = {}
	accumilativeCost = {}
	previousVisits[start] = None 
	accumilativeCost[start] = 0

	while not nodeLoad.empty():
		current = nodeLoad.get()

		if current == exit:
			break
		#TODO: apparently python's default hash will not always return the same values

		#generate states for all the "neighbours" (possible moves)
		neighbies = getAdjacentTiles(current)
		for next in neighbies:
			newCost = accumilativeCost[current] + 1 #all step costs will be one

			if next not in accumilativeCost or newCost < accumilativeCost[next]:
				accumilativeCost[next] = newCost 
				priority = newCost + heuristic(next, exit) #we can just hardcode this dun really matter
				nodeLoad.put(next,priority)
				previousVisits[next] = current 

	return previousVisits, accumilativeCost

def getMoveFromPieces(move, boardPieces):
	mov = generateAllPiecesAsTuples(move)
	board = generateAllPiecesAsTuples(boardPieces)

	if mov == board:
		return
	
	for piece in board:
		if piece not in mov:
			fro = piece

	for piece in mov:
		if piece not in board:
			to = piece

	if len(board) > len(mov):
		return ("EXIT",fro)
	else:
		#TODO: fix error that sometimes occurs here - I think it has something to do with exiting actions
		tiles = getAdjacentTiles(fro)
		if to in tiles:
			return ("MOVE",(fro,to))
		else:
			for tile in tiles:
				if to in getAdjacentTiles(tile):
					return("JUMP",(fro,to))

	return ("PASS", None)

def generateBoardFromMove(color,move,board):
	newBoard = []
	for piece in board:
		#TODO: need this to work for exit and pass actions etc etc
		#TODO: make this work for jumps
		if (piece.column,piece.row) in move[1]:
			newBoard.append(Piece(piece.colour,move[1][1][0],move[1][1][1]))
		else:
			newBoard.append(piece)
	return newBoard

def evaluatePosition(currentColour,board, thisMove,numPlayers): #SHOULD evaluate jumps to be fuckin baller and otherwise move our pieces closer to theirs
	#evaluates position to the colour that is not next (next player has best chance to f u over)
	if numPlayers == 2:
		other = getNextColour(currentColour, True)
		otherer = getNextColour(currentColour)
		if checkPieceHasColours(other,board):
			otherColour = other
		elif checkPieceHasColours(otherer,board):
			otherColour = otherer
	else:
		nextColour = getNextColour(currentColour)
		otherColour = getNextColour(currentColour,True)
	#TODO: make metrics slightly different for 2 or 3 players
	#nextColour = self.getNextColour(currentColour)
	score = 0

	us = getPiecesOfColour(board,currentColour)

	#We are telling the program that a jump is good if it is not over our own piece
	if "JUMP" in thisMove:
		inUs = False
		for piece in us:
			mid = middleHex(thisMove)
			if(piece.column,piece.row) == mid:
				inUs = True
				break
		if not inUs:
			score += 1
	
	#TODO: having a piece in us in adjacent tiles is worth points, want the bois on our flanks
	#TODO: BIG TODO: make all code work by passing in a board instead so we can use the "get_mid_hex" method
	value = 0
	boiSupportMetric = 0
	for p in us:
		tiles = getAdjacentTiles((p.column,p.row))
		for q in us:
			#if q in tiles:
				#boiSupportMetric += 3
			value += heuristic((q.column,q.row),(p.column,p.row))
	if value > 0:
		value = 20/value
	
	score += value
	score += boiSupportMetric
	#HERE WE WANT THE VALUE TO BE A MIX OF: taking a piece is good as fuck, and getting our pieces in proximity of other pieces is good as fuck
	return score

def middleHex(move):

	jumpedFrom = move[1][0]
	jumpedTo = move[1][1]

	tiles = getAdjacentTiles(jumpedFrom)

	for tile in tiles:
		if jumpedTo in getAdjacentTiles(tile):
			midPeece = tile

	return midPeece

def heuristic(tup, other):
	(x1, y1) = tup
	(x2, y2) = other
	return ((abs(x1-x2) + abs(x1 + y1 - x2 - y2) + abs(y1-y2))/2)

def getNextColour(current, notNext=False):
	if current == "red":
		if notNext:
			return "green"
		return "blue"
	elif current == "blue":
		if notNext:
			return "red"
		return "green"
	elif current == "green":
		if notNext:
			return "blue"
		return "red"
	else:
		return None

def checkPieceHasColours(ourColour, board):
	for p in board:
		if p.colour == ourColour:
			return True
	return False

def generateAllPiecesAsTuples(board):
	tups = []
	for piece in board:
		tups.append((piece.column,piece.row))
	return tups

def generateMoves(board, colour, exits):
	moves=[]
	myPieces = getPiecesOfColour(board, colour)
	
	for piece in myPieces:
		tempMove = getPossibleMoves(piece,exits,generateAllPiecesAsTuples(board))
		for move in tempMove:
			moves.append(move)

	return moves

def getPiecesOfColour(board, colour):
	allP = []
	for pie in board:
		if pie.colour == colour:
			allP.append(pie)
	return allP

def getPossibleMoves(piece,exits,allPieces):
	moveList = []
	
	tupl = (piece.column,piece.row)

	if tupl in exits:
		moveList.append(("EXIT",tupl)) 

	topLeft = calcTopLeft(tupl)
	topRight = calcTopRight(tupl)
	left = calcLeft(tupl)
	right = calcRight(tupl)
	bottomLeft = calcBottomLeft(tupl)
	bottomRight = calcBottomRight(tupl)

	if topLeft != (99,99):
		if topLeft in allPieces:
			jumpHex = calcTopLeft(topLeft)
			if jumpHex != (99,99):
				if jumpHex not in allPieces:
					moveList.append(('JUMP',(tupl,jumpHex)))
		else:
			moveList.append(('MOVE',(tupl,topLeft)))

	if topRight != (99,99):
		if topRight in allPieces:
			jumpHex = calcTopRight(topRight)
			if jumpHex != (99,99):
				if jumpHex not in allPieces:
					moveList.append(('JUMP',(tupl,jumpHex)))
		else:
			moveList.append(('MOVE',(tupl,topRight)))

	if left != (99,99):
		if left in allPieces:
			jumpHex = calcLeft(left)
			if jumpHex != (99,99):
				if jumpHex not in allPieces:
					moveList.append(('JUMP',(tupl,jumpHex)))
		else:
			moveList.append(('MOVE',(tupl,left)))

	if right != (99,99):
		if right in allPieces:
			jumpHex = calcRight(right)
			if jumpHex != (99,99):
				if jumpHex not in allPieces:
					moveList.append(('JUMP',(tupl,jumpHex)))
		else:
			moveList.append(('MOVE',(tupl,right)))

	if bottomLeft != (99,99):
		if bottomLeft in allPieces:
			jumpHex = calcBottomLeft(bottomLeft)
			if jumpHex != (99,99):
				if jumpHex not in allPieces:
					moveList.append(('JUMP',(tupl,jumpHex)))
		else:
			moveList.append(('MOVE',(tupl,bottomLeft)))

	if bottomRight != (99,99):
		if bottomRight in allPieces:
			jumpHex = calcBottomRight(bottomRight)
			if jumpHex != (99,99):
				if jumpHex not in allPieces:
					moveList.append(('JUMP',(tupl,jumpHex)))
		else:
			moveList.append(('MOVE',(tupl,bottomRight)))

	return moveList

def getExits(colour):
	if colour == "red":
		return [(3,-3),(3,-2),(3,-1),(3,0)]
	elif colour == "green":
		return [(-3,3),(-2,3),(-1,3),(0,3)]
	elif colour == "blue":
		return [(-3,0),(-2,-1),(-1,-2),(0,-3)]

def getAdjacentTiles(tupl):

	tiles = []

	topLeft = calcTopLeft(tupl)
	topRight =calcTopRight(tupl)
	left = calcLeft(tupl)
	right = calcRight(tupl)
	bottomLeft = calcBottomLeft(tupl)
	bottomRight = calcBottomRight(tupl)

	if topLeft != (99,99):
		tiles.append(topLeft)
	if topRight != (99,99):
		tiles.append(topRight)
	if left != (99,99):
		tiles.append(left)
	if right != (99,99):
		tiles.append(right)
	if bottomLeft != (99,99):
		tiles.append(bottomLeft)
	if bottomRight != (99,99):
		tiles.append(bottomRight)

	return tiles

def calcTopLeft(tupl):
	if tupl==(-3,0) or tupl==(-2,-1) or tupl==(-1,-2) or tupl==(0,-3) or tupl==(1,-3) or tupl==(2,-3) or tupl==(3,-3):
		topLeft = (99,99)
	else:
		topLeft = (tupl[0], tupl[1]-1)
	return topLeft

def calcTopRight(tupl):
	if tupl==(0,-3) or tupl==(1,-3) or tupl==(2,-3) or tupl==(3,-3) or tupl==(3,-2) or tupl==(3,-1) or tupl==(3,0):
		topRight = (99,99)
	else:
		topRight = (tupl[0]+1, tupl[1]-1)
	return topRight

def calcLeft(tupl):
	if tupl==(-3,0) or tupl==(-2,-1) or tupl==(-1,-2) or tupl==(0,-3) or tupl==(-3,1) or tupl==(-3,2) or tupl==(-3,3):
		left = (99,99)
	else:
		left = (tupl[0]-1, tupl[1])
	return left

def calcRight(tupl):
	if tupl==(3,-3) or tupl==(3,-2) or tupl==(3,-1) or tupl==(3,0) or tupl==(2,1) or tupl==(1,2) or tupl==(0,3):
		right = (99,99)
	else:
		right = (tupl[0]+1, tupl[1])
	return right

def calcBottomLeft(tupl):
	if tupl==(-3,0) or tupl==(-3,1) or tupl==(-3,2) or tupl==(-3,3) or tupl==(-2,3) or tupl==(-1,3) or tupl==(0,3):
		bottomLeft = (99,99)
	else:
		bottomLeft = (tupl[0]-1, tupl[1]+1)
	return bottomLeft

def calcBottomRight(tupl):
	if tupl==(-3,3) or tupl==(-2,3) or tupl==(-1,3) or tupl==(0,3) or tupl==(1,2) or tupl==(2,1) or tupl==(3,0):
		bottomRight = (99,99)
	else:
		bottomRight = (tupl[0], tupl[1]+1)
	return bottomRight

class Piece:

	def __init__ (self, colour, column, row):
		self.colour = colour
		self.row = row
		self.column = column

class Board:

	RED = "red"
	GREEN = "blue"
	BLUE = "green"

	def __init__ (self, input_layout = None):

		#if no input_layoout is specified, create the board specified by the input dict
		if input_layout:
			#__TODO__
			return
		#otherwise set up the default board
		else:
			self.pieces = self.generatePieces()

	def generatePieces(self): #helper function to generate pieces for all players
		pieces = []
		#create each colour of pieces in this order, R, G, B
		# all 4 red pieces 
		pieces.append(Piece(self.RED, -3,0))
		pieces.append(Piece(self.RED, -3,1))
		pieces.append(Piece(self.RED, -3,3))
		pieces.append(Piece(self.RED, -3,2))
		# all 4 green pieces 
		pieces.append(Piece(self.GREEN, 0,-3))
		pieces.append(Piece(self.GREEN, 1,-3))
		pieces.append(Piece(self.GREEN, 2,-3))
		pieces.append(Piece(self.GREEN, 3,-3))
		# all 4 blue pieces
		pieces.append(Piece(self.BLUE, 0, 3))
		pieces.append(Piece(self.BLUE, 1, 2))
		pieces.append(Piece(self.BLUE, 2, 1))
		pieces.append(Piece(self.BLUE, 3, 0))

		return pieces

	#update the board state based on an action taken by a player of a given colour
	def update(self, colour, action):
		#TODO: keep track of which pieces are exiting and winning, because this is the colour we want to target
		if action[0] == "PASS":
			return
		elif action[0] == "MOVE":
			self.move_piece(action[1][0], action[1][1])
		elif action[0] == "JUMP":
			self.jump_piece(action[1][0], action[1][1], colour)
		elif action[0] == "EXIT":
			self.delete_piece(action[1])

	def move_piece(self, piece, moveTo):
		for p in self.pieces:
			if (p.column,p.row) == piece:
				p.column = moveTo[0]
				p.row = moveTo[1]
				return

	# jumps a piece from pos_i to pos_f, then changes the colour of the piece that was jumped
	def jump_piece(self, piece, moveTo, colour):
		for p in self.pieces:
			if (p.column,p.row) == piece:
				p.column = moveTo[0]
				p.row = moveTo[1]
			elif (p.column,p.row) == self.mid_hex(piece,moveTo):
				p.colour = colour

	def delete_piece(self, piece):
		for p in self.pieces:
			if (p.column,p.row) == piece:
				self.pieces.remove(p)

	def mid_hex(self,pieceFrom,pieceTo):
		tiles = getAdjacentTiles(pieceFrom)

		for tile in tiles:
			if pieceTo in getAdjacentTiles(tile):
				midPeece = tile

		return midPeece