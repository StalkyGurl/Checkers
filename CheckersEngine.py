'''
This file is responsible for storing all the information about the current state of the game.
It is also responsible for checking and returning all the valid moves. It also contains move log.
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
        self.moves = [] # all non-capture valid moves
        self.moveLog = []
        self.firstCaptureMoves = [] # all capture valid moves
        self.nextCaptureMoves = [] # the list of next captures for a moved pawn
        self.whiteWon = False
        self.blackWon = False


    '''
    Function responsible for making a move.
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '-'
        if move.endRow == 0 and move.pawnMoved == 'w':
            self.board[move.endRow][move.endCol] = 'W'
            move.isUpdateMove = True
        elif move.endRow == 7 and move.pawnMoved == 'b':
            self.board[move.endRow][move.endCol] = 'B'
            move.isUpdateMove = True
        else:
            self.board[move.endRow][move.endCol] = move.pawnMoved
        if move.isCaptureMove:
            self.board[move.capturedSquare[0]][move.capturedSquare[1]] = '-'
        self.moveLog.append(move)

    
    '''
    Function for undoing moves
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            self.whiteWon = False
            self.blackWon = False
            move = self.moveLog.pop()
            if move.movedQueen:
                self.board[move.startRow][move.startCol] = 'B' if self.whitesTurn else 'W'
            else:
                self.board[move.startRow][move.startCol] = 'b' if self.whitesTurn else 'w'
            self.board[move.endRow][move.endCol] = '-'
            if move.isCaptureMove:
                if move.capturedQueen:
                    self.board[move.capturedSquare[0]][move.capturedSquare[1]] = 'W' if self.whitesTurn else 'B'
                else:
                    self.board[move.capturedSquare[0]][move.capturedSquare[1]] = 'w' if self.whitesTurn else 'b'
                if move.lastCapture:
                    self.whitesTurn = not self.whitesTurn
            else:
                self.whitesTurn = not self.whitesTurn

    '''
    Function for reseting game state.
    '''
    def restartGame(self):
        self.board = [
            ['-', 'b', '-', 'b', '-', 'b', '-', 'b'],
            ['b', '-', 'b', '-', 'b', '-', 'b', '-'],
            ['-', 'b', '-', 'b', '-', 'b', '-', 'b'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['w', '-', 'w', '-', 'w', '-', 'w', '-'],
            ['-', 'w', '-', 'w', '-', 'w', '-', 'w'],
            ['w', '-', 'w', '-', 'w', '-', 'w', '-']
        ] # reset the board
        self.whitesTurn = True # it's whites turn
        self.moves = [] # clear moves
        self.moveLog = [] # clear moveLog
        self.firstCaptureMoves = [] 
        self.nextCaptureMoves = []
        self.whiteWon = False
        self.blackWon = False


    '''
    This function is checking if there is any capture move possible.
    '''
    def CapturePossible(self):
        DIRECTIONS = ((1,1),(-1,-1),(1,-1),(-1,1))
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] != '-':
                    if (self.board[r][c] == 'w' and self.whitesTurn) or (self.board[r][c] == 'b' and not self.whitesTurn):
                        for d in DIRECTIONS:
                            if 0 <= r + d[0] < DIMENSION and 0 <= r + d[0] + d[0] < DIMENSION \
                                and 0 <= c + d[1] < DIMENSION and 0 <= c + d[1] + d[1] < DIMENSION:

                                if ((self.board[r + d[0]][c + d[1]] == 'b' or self.board[r + d[0]][c + d[1]] == 'B') \
                                    and self.whitesTurn) or ((self.board[r + d[0]][c + d[1]] == 'w' or \
                                    self.board[r + d[0]][c + d[1]] == 'W') and not self.whitesTurn):

                                    if self.board[r + d[0] + d[0]][c + d[1] + d[1]] == '-':
                                        return True
                                    
                    elif (self.board[r][c] == 'W' and self.whitesTurn) or (self.board[r][c] == 'B' and not self.whitesTurn):
                        for d in DIRECTIONS:
                            for i in range(1, DIMENSION):
                                enemy_row = r + d[0] * i
                                enemy_col = c + d[1] * i
                                empty_row = enemy_row + d[0]
                                empty_col = enemy_col + d[1]
                                if empty_row >= 0 and empty_row < DIMENSION and empty_col >= 0 and empty_col < DIMENSION:
                                    if self.board[enemy_row][enemy_col] != '-' and self.board[empty_row][empty_col] != '-':
                                        break

                                    elif ((self.board[enemy_row][enemy_col] == 'b' or self.board[enemy_row][enemy_col] == 'B') and \
                                         self.whitesTurn) or ((self.board[enemy_row][enemy_col] == 'w' \
                                        or self.board[enemy_row][enemy_col] == 'W') and not self.whitesTurn):
                                        if self.board[empty_row][empty_col] == '-':
                                            return True
        return False


    '''
    This functions searches for all the valid moves (if there is no capture possible) for the current game state.
    '''
    def getValidMoves(self):
        for r in range(len(self.board[0])):
            for c in range(len(self.board[r])):
                if self.board[r][c] != '-':
                    if self.board[r][c] == 'w' and self.whitesTurn:
                        if r - 1 >= 0 and r - 1 < DIMENSION and c + 1 >= 0 and c + 1 < DIMENSION:
                            newRow = r - 1
                            newCol = c + 1
                            if self.board[newRow][newCol] == '-':
                                move = Move((r, c),(newRow, newCol), self.board)
                                if move not in self.moves:
                                    self.moves.append(move)
                        if r - 1 >= 0 and r - 1 < DIMENSION and c - 1 >= 0 and c - 1 < DIMENSION:
                            newRow = r - 1
                            newCol = c - 1
                            if self.board[newRow][newCol] == '-':                                
                                move = Move((r, c),(newRow, newCol), self.board)
                                if move not in self.moves:
                                    self.moves.append(move)
                    elif self.board[r][c] == 'b' and not self.whitesTurn:
                        if r + 1 >= 0 and r + 1 < DIMENSION and c + 1 >= 0 and c + 1 < DIMENSION:
                            newRow = r + 1
                            newCol = c + 1
                            if self.board[newRow][newCol] == '-': 
                                move = Move((r, c),(newRow, newCol), self.board)
                                if move not in self.moves:
                                    self.moves.append(move)
                        if r + 1 >= 0 and r + 1 < DIMENSION and c - 1 >= 0 and c - 1 < DIMENSION:
                            newRow = r + 1
                            newCol = c - 1
                            if self.board[newRow][newCol] == '-': 
                                move = Move((r, c),(newRow, newCol), self.board)
                                if move not in self.moves:
                                    self.moves.append(move)
                    if (self.board[r][c] == 'W' and self.whitesTurn) or (self.board[r][c] == 'B' and not self.whitesTurn):
                        DIRECTIONS = ((1,1),(-1,-1),(1,-1),(-1,1))
                        for d in DIRECTIONS:
                            for i in range(1, DIMENSION):
                                new_row = r + d[0] * i
                                new_col = c + d[1] * i
                                if new_row >= 0 and new_row < DIMENSION and new_col >= 0 and new_col < DIMENSION:
                                    if self.board[new_row][new_col] == '-':
                                        move = Move((r, c),(new_row, new_col), self.board, movedQueen=True)
                                        if move not in self.moves:
                                            self.moves.append(move)    
                                    else:
                                        break


    '''
    This functions searches for all first valid capture moves.
    '''
    def getFirstCaptureMoves(self):
        DIRECTIONS = ((1,1),(-1,-1),(1,-1),(-1,1))
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] != '-':
                    if (self.board[r][c] == 'w' and self.whitesTurn) or (self.board[r][c] == 'b' and not self.whitesTurn):
                        for d in DIRECTIONS:
                            if 0 <= r + d[0] + d[0] < DIMENSION and 0 <= r + d[0] + d[0] < DIMENSION and 0 <= c + d[1] + d[1] < DIMENSION and \
                                0 <= c + d[1] + d[1] < DIMENSION:

                                if ((self.board[r + d[0]][c + d[1]] == 'b' or self.board[r + d[0]][c + d[1]] == 'B') and \
                                     self.whitesTurn) or ((self.board[r + d[0]][c + d[1]] == 'w' or self.board[r + d[0]][c + d[1]] == 'W') and \
                                     not self.whitesTurn):
                                    
                                    if self.board[r + d[0] + d[0]][c + d[1] + d[1]] == '-':
                                        captured = (r + d[0], c + d[1])
                                        move = Move((r, c),(r + d[0] + d[0], c + d[1] + d[1]), self.board, isCaptureMove = True,
                                                    capturedSquare=captured, capturedQueen=(self.board[captured[0]][captured[1]]== 'W' or \
                                                         self.board[captured[0]][captured[1]]=='B'))
                                        if move not in self.firstCaptureMoves:
                                            self.firstCaptureMoves.append(move)

                    elif (self.board[r][c] == 'W' and self.whitesTurn) or (self.board[r][c] == 'B' and not self.whitesTurn):
                        for d in DIRECTIONS:
                            for i in range(1, DIMENSION):
                                enemy_row = r + d[0] * i
                                enemy_col = c + d[1] * i
                                empty_row = enemy_row + d[0]
                                empty_col = enemy_col + d[1]
                                if empty_row >= 0 and empty_row < DIMENSION and empty_col >= 0 and empty_col < DIMENSION:
                                    if self.board[enemy_row][enemy_col] != '-' and self.board[empty_row][empty_col] != '-':
                                        break

                                    elif ((self.board[enemy_row][enemy_col] == 'b' or self.board[enemy_row][enemy_col] == 'B') and self.whitesTurn) \
                                        or ((self.board[enemy_row][enemy_col] == 'w' or self.board[enemy_row][enemy_col] == 'W') and \
                                        not self.whitesTurn):

                                        if self.board[empty_row][empty_col] == '-':
                                            captured = (enemy_row, enemy_col)
                                            move = Move((r, c),(empty_row, empty_col), self.board, isCaptureMove = True,
                                                    capturedSquare=captured, movedQueen=True, capturedQueen=(self.board[captured[0]][captured[1]]== 'W' or \
                                                                                                              self.board[captured[0]][captured[1]]=='B'))
                                            if move not in self.firstCaptureMoves:
                                                self.firstCaptureMoves.append(move)
                                            break       


'''
This is a move class that contains info about the move - start and end location, ID, info about captures etc.
'''
class Move():
    def __init__(self, startSquare, endSquare, board, capturedSquare=(), isCaptureMove=False, movedQueen=False, capturedQueen=False):
        self.startRow = startSquare[0]
        self.startCol = startSquare[1]
        self.endRow = endSquare[0]
        self.endCol = endSquare[1]
        self.pawnMoved = board[self.startRow][self.startCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        self.isCaptureMove = isCaptureMove
        self.capturedSquare = capturedSquare
        self.isUpdateMove = False # when a pawn gets to the end of the board and becomes a queen
        self.lastCapture = False
        self.movedQueen = movedQueen
        self.capturedQueen = capturedQueen


    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


'''
This function checks if there are more captures possible for a pawn.
'''
def moreCapturesAvalible(board, r, c, gm):
    DIRECTIONS = ((1,1),(-1,-1),(1,-1),(-1,1))
    if (board[r][c] == 'w' and gm.whitesTurn) or (board[r][c] == 'b' and not gm.whitesTurn):
        for d in DIRECTIONS:
            if 0 <= r + d[0] + d[0] < DIMENSION and 0 <= r + d[0] + d[0] < DIMENSION and 0 <= c + d[1] + d[1] < DIMENSION and \
                0 <= c + d[1] + d[1] < DIMENSION:

                if board[r + d[0]][c + d[1]] == 'b' or board[r + d[0]][c + d[1]] == 'B' \
                    if gm.whitesTurn else board[r + d[0]][c + d[1]] == 'w' or board[r + d[0]][c + d[1]] == 'W':
                    
                        if board[r + d[0] + d[0]][c + d[1] + d[1]] == '-':
                            return True
                    
    elif (board[r][c] == 'W' and gm.whitesTurn) or (board[r][c] == 'B' and not gm.whitesTurn):
        for d in DIRECTIONS:
            for i in range(1, DIMENSION):
                enemy_row = r + d[0] * i
                enemy_col = c + d[1] * i
                empty_row = enemy_row + d[0]
                empty_col = enemy_col + d[1]
                if empty_row >= 0 and empty_row < DIMENSION and empty_col >= 0 and empty_col < DIMENSION:
                    if board[enemy_row][enemy_col] != '-' and board[empty_row][empty_col] != '-':
                        break

                    elif board[enemy_row][enemy_col] == 'b' or board[enemy_row][enemy_col] == 'B' \
                        if gm.whitesTurn else board[enemy_row][enemy_col] == 'w' or board[enemy_row][enemy_col] == 'W':
                        
                        if board[empty_row][empty_col] == '-':
                            return True
    return False


'''
This functions searches for all the next valid capture moves.
'''
def getMoreCaptures(board, r, c, gm):
    DIRECTIONS = ((1,1),(-1,-1),(1,-1),(-1,1))
    if (board[r][c] == 'w' and gm.whitesTurn) or (board[r][c] == 'b' and not gm.whitesTurn):
        for d in DIRECTIONS:
            if 0 <= r + d[0] +d[0] < DIMENSION and 0 <= r + d[0] + d[0] < DIMENSION and 0 <= c + d[1] + d[1] < DIMENSION \
                and 0 <= c + d[1] + d[1] < DIMENSION:

                if board[r + d[0]][c + d[1]] == 'b' or board[r + d[0]][c + d[1]] == 'B' \
                    if gm.whitesTurn else board[r + d[0]][c + d[1]] == 'w' or board[r + d[0]][c + d[1]] == 'W':
                    
                    if board[r + d[0] + d[0]][c + d[1] + d[1]] == '-':
                        captured = (r + d[0], c + d[1])
                        move = Move((r, c),(r + d[0] + d[0], c + d[1] + d[1]), board, isCaptureMove = True, capturedSquare=captured, capturedQueen=(board[captured[0]][captured[1]]== 'W' or \
                                                                                                                                                     board[captured[0]][captured[1]]=='B'))
                        if move not in gm.nextCaptureMoves:
                            gm.nextCaptureMoves.append(move)

    elif (board[r][c] == 'W' and gm.whitesTurn) or (board[r][c] == 'B' and not gm.whitesTurn):
        for d in DIRECTIONS:
            for i in range(1, DIMENSION):
                enemy_row = r + d[0] * i
                enemy_col = c + d[1] * i
                empty_row = r + d[0] * i + d[0]
                empty_col = c + d[1] * i + d[1]
                if empty_row >= 0 and empty_row < DIMENSION and empty_col >= 0 and empty_col < DIMENSION:
                    if board[enemy_row][enemy_col] != '-' and board[empty_row][empty_col] != '-':
                        break
                    
                    elif board[enemy_row][enemy_col] == 'b' or board[enemy_row][enemy_col] == 'B' \
                        if gm.whitesTurn else board[enemy_row][enemy_col] == 'w' or board[enemy_row][enemy_col] == 'W':
                        if board[empty_row][empty_col] == '-':
                            captured = (enemy_row, enemy_col)
                            move = Move((r, c),(empty_row, empty_col), board, isCaptureMove = True, capturedSquare=captured, movedQueen=True, capturedQueen=(board[captured[0]][captured[1]]== 'W' or \
                                                                                                                                                              board[captured[0]][captured[1]]=='B'))
                        if move not in gm.nextCaptureMoves:
                            gm.nextCaptureMoves.append(move)