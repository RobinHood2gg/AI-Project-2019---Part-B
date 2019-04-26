import sys

class Player:

	def __init__ (self, colour):
		self.colour = colour
		self.board = Board()
		self.pieces = getPieces() #not sure if this is that useful but chucked her in anyway

	def action(self):
		#TODO: write the code here for our actual parts of the program

		return

	def update(self, colour, action):
		self.board.update(colour, action)

	def getPieces(): #helper function to return current pieces
		pizzi = []
		for piece in board.pieces:
			if piece.colour == colour:
				pizzi.append(piece)
		return pizzi