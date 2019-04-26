import sys 


class Tile:
	def __init__(self, exit, row, column):
		self.exit = exit #character of colour who's exit it is, or none if it is not an exit
		self.row = row
		self.column = column

	def get_neighbours():
		#TODO: find all neighbours and dont return any illegal moves