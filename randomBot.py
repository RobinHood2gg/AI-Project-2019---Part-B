import sys
import json
from random import randint

#hell yeah randomBot works
class Player:

    def __init__ (self, colour):
        self.colour=colour
        self.board = generateBoard()
        self.exits = getExits(colour)

	
    def action(self):
        if self.board == None:
            return ("PASS", None)
        if len(self.board) == 0:
            return ("PASS", None)

        moves = generateMoves(self.board, self.colour, self.exits)
        if(len(moves)==0):
            return ("PASS", None)

        movve = randint(0,len(moves)-1)

        #TODO: fix bug where pieces are disappering from moves?
        return moves[movve]


    def update(self, colour, action):
        self.board = updateBoard(self.board,colour,action)


def generateMoves(board, colour, exits):
    #TODO: fix bug where it says moves exist that dont
    moves=[]
    allPieces = getAllPieces(board)

    for piece in board[colour]:
        tempMov = getPossibleMoves(piece,exits,allPieces)
        for move in tempMov:
            moves.append(move)

    #print(moves)
    return moves

def getAllPieces(board):
    allP = []
    for col in board:
        for pie in board[col]:
            allP.append(pie)
    return allP

def getPossibleMoves(tupl,exits, allPieces):
    moveList = []
    
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

def generateBoard():
    board = {}

    board["red"] = [(-3,0),(-3,1),(-3,2),(-3,3)]
    board["green"] = [(0,-3),(1,-3),(2,-3),(3,-3)]
    board["blue"] = [(0,3),(1,2),(2,1),(3,0)]

    return board

def updateBoard(board,colour,move):
    #need to update for if a piece is jumped
    if "PASS" in move:
        return board

    if "JUMP" in move:
        jumpTo = move[1][1]
        jumpedFrom = move[1][0]

        tiles = getAdjacentTiles(jumpedFrom)

        for tile in tiles:
            if jumpTo in getAdjacentTiles(tile):
                midPeece = tile
                break

        for col in board:
            if midPeece in board[col] and col != colour:
                board[col].remove(midPeece)
                board[colour].append(midPeece)

    if "EXIT" in move:
        for piece in board[colour]:
            if move[1] == piece:
                board[colour].remove(piece)
    else:    
        for piece in board[colour]:
            if piece in move[1]:
                board[colour].remove(piece)
                board[colour].append(move[1][1])

    return board

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