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