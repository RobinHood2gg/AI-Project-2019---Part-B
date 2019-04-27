import sys

class Piece:
	def __init__ (self, colour, row, column):
		self.colour = colour
		self.row = row
		self.column = column

	#check if target hex is directly adjacent to self
	def is_adjacent(target_row, target_column):
		if (self.row+1 == target_row) or (self.row-1 == target_row):
			if (self.column+1 == target_column) or (self.colour-1 == target_column):
				return True
		return False

	def is_jump_adjacent(target_row, target_column):
		#check jump which is along the same row
		if self.row == target_row:
			if (self.column+2 == target_column) or (self.column-2 == target_column):
				return True

		#check jump which is alont the same column
		elif self.column == target_column:
			if (self.row+2 == target_row) or (self.row-2 == target_row):
				return True
		#check case where the jump is accross both row and colum
		else:
			if (self.row+2 == target_row) and (self.column-2 == target_column):
				return True
			elif (self.row-2 == target_row) and (self.column+2 == target_column):
				return True
		#all other cases are a invalid jump		
		return False

	def getPossibleMoves(board, ourPieces): 

    	myList = []
		tupl = (this.row,this.column)

    	if board.tiles[tupl] != None:
        	myList.append(("EXIT",tupl,(69,69))) 
			#we DONT want to return here as we still have possible moves we can make. Not useful to always exit in part B
    
   		topLeft = calcTopLeft(tupl)
	    topRight = calcTopRight(tupl)
    	left = calcLeft(tupl)
	    right = calcRight(tupl)
    	bottomLeft = calcBottomLeft(tupl)
	    bottomRight = calcBottomRight(tupl)

    	if topLeft != (99,99): #we have an out of bounds thingo
        	if topLeft in board.pieces and topLeft not in ourPieces: #a jump is possible
            	jumpHex = calcTopLeft(topLeft)
            	if jumpHex != (99,99):
                	if jumpHex not in board.pieces: #if the jump hex is empty we want to add it to the array
                    	myList.append(("JUMP",tupl,jumpHex))
        	else:
            	myList.append(("MOVE",tupl,topLeft))

		if topRight != (99,99): #we have an out of bounds thingo
			if topRight in board.pieces and topRight not in ourPieces: #a jump is possible
				jumpHex = calcTopRight(topRight)
				if jumpHex != (99,99):
					if jumpHex not in board.pieces: #if the jump hex is empty we want to add it to the array
						myList.append(("JUMP",tupl,jumpHex))
			else:
				myList.append(("MOVE",tupl,topRight))

		if left != (99,99): #we have an out of bounds thingo
			if left in board.pieces and left not in ourPieces: #a jump is possible
				jumpHex = calcLeft(left)
				if jumpHex != (99,99):
					if jumpHex not in board.pieces: #if the jump hex is empty we want to add it to the array
						myList.append(("JUMP",tupl,jumpHex))
			else:
				myList.append(("MOVE",tupl,left))

		if right != (99,99): #we have an out of bounds thingo
			if right in board.pieces and right not in ourPieces #a jump is possible
				jumpHex = calcRight(right)
				if jumpHex != (99,99):
					if jumpHex not in board.pieces: #if the jump hex is empty we want to add it to the array
						myList.append(("JUMP",tupl,jumpHex))
			else:
				myList.append(("MOVE",tupl,right))

		if bottomLeft != (99,99): #we have an out of bounds thingo
			if bottomLeft in board.pieces and bottomLeft not in ourPieces: #a jump is possible
				jumpHex = calcBottomLeft(bottomLeft)
				if jumpHex != (99,99):
					if jumpHex not in board.pieces: #if the jump hex is empty we want to add it to the array
						myList.append(("JUMP",tupl,jumpHex))
			else:
				myList.append(("MOVE",tupl,bottomLeft))

		if bottomRight != (99,99): #we have an out of bounds thingo
			if bottomRight in board.pieces and bottomRight not in ourPieces: #a jump is possible
				jumpHex = calcBottomRight(bottomRight)
				if jumpHex != (99,99):
					if jumpHex not in board.pieces: #only cant jump if there are 2 pieces in a row or jump to space is null, otherwise we are good
						myList.append(("JUMP",tupl,jumpHex))
			else:
				myList.append(("MOVE",tupl,bottomRight))

    	return myList 
	
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