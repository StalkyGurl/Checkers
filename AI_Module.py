'''
This file stores all functions and mechanics for the AI.
'''

import pygame as p
from random import randint, shuffle, random
from CheckersEngine import *
from board import *

DEPTH = 2


'''
This function chooses a random valid move for the AI.
'''
def AIMove(gs, capturePossible=False, firstCapture=False):
    global nextMove
    # if no capture possible
    if not capturePossible:
        gs.getValidMoves()
        ValidMoves = gs.moves
        if len(ValidMoves) == 0: 
            if gs.whitesTurn: gs.blackWon = True
            else: gs.whiteWon = True
        else:
            AImove = findBestMove(gs, ValidMoves)
            return AImove
    elif capturePossible and firstCapture:
        gs.getFirstCaptureMoves()
        ValidMoves = gs.moves
        return ValidMoves[randint(0, len(ValidMoves)-1)]
    elif capturePossible and not firstCapture:
        ValidMoves = gs.moves
        return ValidMoves[randint(0, len(ValidMoves)-1)]


'''
This function calculates the score of the pawns on board.
'''
def evaluateMaterial(gs):
    score = 0
    for r in range(len(gs.board)):
        for c in range(len(gs.board[r])):
            if gs.board[r][c] == 'w':
                score += 1
            elif gs.board[r][c] == 'W':
                score += 10
            elif gs.board[r][c] == 'b':
                score -= 1
            elif gs.board[r][c] == 'B':
                score -= 10
    return score


'''
This function calculates the score of the pawn's positions.
'''
def evaluatePosition(gs):
    score = 0
    DIRECTIONS = [(1,1),(-1,-1),(1,-1),(-1,1)]
    for r in range(len(gs.board)):
        for c in range(len(gs.board[r])):
            if gs.board[r][c] == 'w' or gs.board[r][c] == 'W' and gs.whitesTurn:
                for d in DIRECTIONS:
                    nr = r + d[0]
                    nc = c + d[1]
                    if 0 <= nr < DIMENSION and 0 <= nc < DIMENSION:
                        if gs.board[nr][nc] == 'b' or gs.board[nr][nc] == 'B':
                            score -= 6
                        elif gs.board[nr][nc] == 'w' or gs.board[nr][nc] == 'W':
                            score += 2
                        elif gs.board[nr][nc] == '-':
                            score -= 4  
            elif gs.board[r][c] == 'b' or gs.board[r][c] == 'B' and not gs.whitesTurn:
                for d in DIRECTIONS:
                    nr = r + d[0]
                    nc = c + d[1]
                    if 0 <= nr < DIMENSION and 0 <= nc < DIMENSION:
                        if gs.board[nr][nc] == 'b' or gs.board[nr][nc] == 'B':
                            score -= 2
                        elif gs.board[nr][nc] == 'w' or gs.board[nr][nc] == 'W':
                            score += 6
                        elif gs.board[nr][nc] == '-':
                            score += 4 
    return score


# scores the board overall
def scoreGameState(gs):
    return evaluateMaterial(gs) + evaluatePosition(gs)


'''
Function that finds the best move for the AI
'''
def findBestMove(gs, ValidMoves):
    shuffle(ValidMoves)
    turn = 1 if gs.whitesTurn else -1
    bestMove = ValidMoves[0]
    maxScore = -10000
    for move in ValidMoves:
        gs.makeMove(move)
        score = turn * scoreGameState(gs) + random() * 0.1
        gs.whitesTurn = not gs.whitesTurn
        gs.undoMove()
        if score > maxScore:
            maxScore = score
            bestMove = move
            print(maxScore)
    gs.moves = []
    return bestMove
        