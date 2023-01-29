'''
This file is responsible for storing all the information about the current state of the game.
It is also responsible for checking and returning all the valid moves.
'''

from board import DIMENSION

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
        self.capturePossible = False #CapturePossible()
        self.moves = []
        self.moveLog = []


    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '-'
        self.board[move.endRow][move.endCol] = move.pawnMoved
        self.moveLog.append(move)
        self.whitesTurn = not self.whitesTurn


    def CapturePossible(self, startRow, startCol):
        if self.whitesTurn:
            pass
        else:
            pass


    def getValidMoves(self):
        if not self.capturePossible:
            for r in range(len(self.board[0])):
                for c in range(len(self.board[r])):
                    if self.board[r][c] != '-':
                        if self.board[r][c] == 'w' and self.whitesTurn:
                            if r - 1 >= 0 and r - 1 < DIMENSION and c + 1 >= 0 and c + 1 < DIMENSION:
                                newRow = r - 1
                                newCol = c + 1
                                if self.board[newRow][newCol] == '-':
                                    self.moves.append(Move((r, c),(newRow, newCol), self.board))
                            if r - 1 >= 0 and r - 1 < DIMENSION and c - 1 >= 0 and c - 1 < DIMENSION:
                                newRow = r - 1
                                newCol = c - 1
                                if self.board[newRow][newCol] == '-':                                
                                    self.moves.append(Move((r, c),(newRow, newCol), self.board))
                        elif self.board[r][c] == 'b' and not self.whitesTurn:
                            if r + 1 >= 0 and r + 1 < DIMENSION and c + 1 >= 0 and c + 1 < DIMENSION:
                                newRow = r + 1
                                newCol = c + 1
                                if self.board[newRow][newCol] == '-': 
                                    self.moves.append(Move((r, c),(newRow, newCol), self.board))
                            if r + 1 >= 0 and r + 1 < DIMENSION and c - 1 >= 0 and c - 1 < DIMENSION:
                                newRow = r + 1
                                newCol = c - 1
                                if self.board[newRow][newCol] == '-': 
                                    self.moves.append(Move((r, c),(newRow, newCol), self.board))
        else:
            while self.capturePossible:
                pass


class Move():
    def __init__(self, startSquare, endSquare, board):
        self.startRow = startSquare[0]
        self.startCol = startSquare[1]
        self.endRow = endSquare[0]
        self.endCol = endSquare[1]
        self.pawnMoved = board[self.startRow][self.startCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    
    def getValidMoves(self, board):
        if not board.capturePossible:
            for r in board[0]:
                for c in board[r]:
                    if board[r][c] != '-':
                        if board[r][c] == 'w' and board.whitesTurn:
                            if r - 1 >= 0 and c + 1 < DIMENSION:
                                newRow = r - 1
                                newCol = c + 1
                                if board[newRow][newCol] == '-':
                                    board.moves.append[Move((r, c),(newRow, newCol), board)]
                            if r - 1 >= 0 and c - 1 < DIMENSION:
                                newRow = r - 1
                                newCol = c + 1
                                if board[newRow][newCol] == '-':                                
                                    board.moves.append[Move((r, c),(newRow, newCol), board)]
                        elif board[r][c] == 'b' and not board.whitesTurn:
                            if r + 1 >= 0 and c + 1 < DIMENSION:
                                newRow = r + 1
                                newCol = c + 1
                                if board[newRow][newCol] == '-': 
                                    board.moves.append[Move((r, c),(newRow, newCol), board)]
                            if r + 1 >= 0 and c - 1 < DIMENSION:
                                newRow = r + 1
                                newCol = c + 1
                                if board[newRow][newCol] == '-': 
                                    board.moves.append[Move((r, c),(newRow, newCol), board)]
        else:
            while board.capturePossible:
                pass

