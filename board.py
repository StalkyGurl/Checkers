'''
This file is responsible for drawing the board depending on the current game state.
'''
from CheckersMain import DIMENSION, SQ_SIZE
from pawns import *
import pygame as p


BG_COLOR = 'lemonchiffon1'
SQ_COLOR = 'ivory4'

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
Responsible for all the graphics within the current game state.
'''
def drawGameState(screen, game_state):
    drawBoard(screen) # draw squares on the board
    drawPawns(screen, game_state.board) # draw pawns

