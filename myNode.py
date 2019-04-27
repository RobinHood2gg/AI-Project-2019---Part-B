import sys

class myNode:

    def __init__(self, pieces, neigh):
        self.peeces = pieces 
        self.neighbours = neigh #neigh is a 
        self.value=0 #minimax value

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