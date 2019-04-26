import sys


class Board:

	RED = 'R'
	GREEN = 'G'
	BLUE = 'B'

	def __init__ (self, input_layout = None):

		#if no input_layoout is specified, create the board specified by the input dict
		if input_layout:
			#__TODO__
			return
		#otherwise set up the default board
		else:
			self.tiles = generateBoard()
			self.pieces = generatePieces()

	def generateBoard(exits): #helper function to generate all board tiles
		tiles = {}

		red = [(3,-3),(3,-2),(3,-1),(3,0)]
		green = [(-3,3),(-2,3),(-1,3),(0,3)]
		blue = [(-3,0),(-3,1),(-3,2),(-3,3)]

		for i in range(-3,4): #(i,j) is the order we have that works
        	if(i<0):
        		for j in range(-3-i,4):
            		if (i,j) in red:
						tiles[(i,j)] = 'R'
					elif (i,j) in green:
						tiles[(i,j)] = 'G'
					elif (i,j) in blue:
						tiles[(i,j)] = 'B'
					else:
						tiles[(i,j)] = None
			else:
    	    	for j in range(-3,4-i):
    	        	if (i,j) in red:
						tiles[(i,j)] = 'R'
					elif (i,j) in green:
						tiles[(i,j)] = 'G'
					elif (i,j) in blue:
						tiles[(i,j)] = 'B'
					else:
						tiles[(i,j)] = None
						
		return tiles

	def generatePieces(): #helper function to generate pieces for all players
		pieces = []
		#create each colour of pieces in this order, R, G, B
		# all 4 red pieces 
		pieces.append(Piece(RED, 0, -3))
		pieces.append(Piece(RED, 1, -3))
		pieces.append(Piece(RED, 3, -3))
		pieces.append(Piece(RED, 2, -3))
		# all 4 green pieces 
		pieces.append(Piece(GREEN, -3, 0))
		pieces.append(Piece(GREEN, -3, 1))
		pieces.append(Piece(GREEN, -3, 2))
		pieces.append(Piece(GREEN, -3, 3))
		# all 4 blue pieces
		pieces.append(Piece(BLUE, 0, 3))
		pieces.append(Piece(BLUE, 1, 2))
		pieces.append(Piece(BLUE, 2, 1))
		pieces.append(Piece(BLUE, 3, 0))

		return pieces

	#update the board state based on an action taken by a player of a given colour
	def update(self, colour, action):
		if action[0] == "PASS":
			return
		elif action[0] == "Move":
			self.move_piece(action[1][0], action[1][1])
		elif action[0] == "Jump":
			self.jump_piece(action[1][0], action[1][1], colour)
		elif action[0] == "Exit":
			self.delete_piece(action[1][0], action[1][1])

	def move_piece(self, pos_i, pos_f):
		#__TODO__

	# jumps a piece from pos_i to pos_f, then changes the colour of the piece that was jumped
	def jump_piece(self, pos_i, pos_f, colour):
		#__TODO__

	def delete_piece(self, q, r):
		#__TODO__

	def mid_hex(row1, column1, row2, column2):
		mid_row =(row1+row2)/2
		mid column = (column1+column2)/2

		return [mid_row, mid_column]

	def is_legal_move(piece, target_row, target,column):
		#check that destination is not occupied by another piece
		for piece in self.pieces:
			if piece.row == target_row:
				return False
			if piece.column == target_column
				return False

		#now check if destination is in range of a regular non juimp move
		if piece.is_adjacent(target_row, target_column):
			return True

		#now check if the piece can jump to get to the destination
		# by checking checking range, then checking that the middle piece is occupied
		if piece.is_jump_adjacent(target_row, target_column):
			mid_hex = mid_hex(piece.row, piece.column, target_row, target_column)
			mid_row = mid_hex[0]
			mid_column = mid_hex[1]

			for piece in pieces:
				if (piece.row == mid_row) and (piece.column == mid_column):
					return True

		#all other cases are not legal moves
		return False