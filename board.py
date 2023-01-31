'''
This file is responsible for drawing the board depending on the current game state.
'''

from pawns import *
import pygame as p


BG_COLOR = 'lemonchiffon1'
SQ_COLOR = 'ivory4'
WIDTH = HEIGHT = 600
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION

'''
Draw the squares on the board.
'''
def drawBoard(screen):
    colors = [BG_COLOR, SQ_COLOR]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Draw the pawns on the board.
'''
def drawPawns(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            pawn = board[r][c]
            if pawn != '-':
                pawn_dict[board[r][c]].drawPawn(screen, c*SQ_SIZE+SQ_SIZE//2, r*SQ_SIZE+SQ_SIZE//2)


'''
This function is for updating the board.
'''
def updateBoard(screen, game_state, FPS, clock, validMoves, sqSelected):
    drawGameState(screen, game_state, validMoves, sqSelected)
    clock.tick(FPS)
    p.display.flip()

'''
Highlight selected squares and all valid moves for this pawn
'''
def highlightSquares(screen, game_state, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if ((game_state.board[r][c] == 'w' or game_state.board[r][c] == 'W') and game_state.whitesTurn) \
            or ((game_state.board[r][c] == 'b' or game_state.board[r][c] == 'B') and not game_state.whitesTurn):
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.fill(p.Color('purple'))
            s.set_alpha(75) # transparency from range 0-255
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # highlight moves from that square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.fill(p.Color('yellow'))
            s.set_alpha(75) # transparency from range 0-255
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))



'''
Responsible for all the graphics within the current game state.
'''
def drawGameState(screen, game_state, validMoves, sqSelected):
    drawBoard(screen) # draw squares on the board
    highlightSquares(screen, game_state, validMoves, sqSelected)
    drawPawns(screen, game_state.board) # draw pawns

