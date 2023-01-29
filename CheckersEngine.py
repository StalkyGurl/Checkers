'''
This file is responsible for storing all the information about the current state of the game.
It is also responsible for checking and returning all the valid moves.
'''

class GameState():
    def __init__(self):
        self.board = [
            ['-', 'b', '-', 'b', '-', 'b', '-', 'b'],
            ['b', '-', 'b', '-', 'b', '-', 'b', '-'],
            ['-', 'b', '-', 'b', '-', 'b', '-', 'b'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['w', '-', 'w', '-', 'w', '-', 'w', '-'],
            ['-', 'w', '-', 'w', '-', 'w', '-', 'w'],
            ['w', '-', 'w', '-', 'w', '-', 'w', '-']
        ]
        self.whitesTurn = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '-'
        self.board[move.endRow][move.endCol] = move.pawnMoved
        self.moveLog.append(move)
        self.whitesTurn = not self.whitesTurn


class Move():
    def __init__(self, startSquare, endSquare, board):
        self.startRow = startSquare[0]
        self.startCol = startSquare[1]
        self.endRow = endSquare[0]
        self.endCol = endSquare[1]
        self.pawnMoved = board[self.startRow][self.startCol]