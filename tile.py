import sys

#I think you're right in that this class is mostly obsolete. Don't need it until/unless we want a heuristic that explicitly considers white space between us and other 
#players

class Tile: 
	def __init__(self, exit, row, column):
		self.exit = exit #character of colour who's exit it is, or none if it is not an exit
		self.row = row
		self.column = column