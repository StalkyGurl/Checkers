'''
This file stores all functions and mechanics for the AI.
'''

import pygame as p
from random import randint
from CheckersEngine import *
from board import *


'''
This function chooses a random valid move for the AI.
'''
def AIrandomMove(gs, capturePossible=False, firstCapture=False):
    # if no capture possible
    if not capturePossible:
        gs.getValidMoves()
        ValidMoves = gs.moves
        if len(ValidMoves) == 0: 
            if gs.whitesTurn: gs.blackWon = True
            else: gs.whiteWon = True
        else:
            AImove = ValidMoves[randint(0, len(ValidMoves)-1)]
            return AImove
    elif capturePossible and firstCapture:
        gs.getFirstCaptureMoves()
        ValidMoves = gs.firstCaptureMoves
        AImove = ValidMoves[randint(0, len(ValidMoves)-1)]
        return AImove
    else:
        ValidMoves = gs.nextCaptureMoves
        AImove = ValidMoves[randint(0, len(ValidMoves)-1)]
        return AImove


