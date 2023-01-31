'''
This is the main driver file.
'''

import pygame as p
from CheckersEngine import *
from board import *
from pawns import *

FPS = 60

'''
The main driver of the code for user input and updating the graphics.
'''
def main():
    p.init()
    p.display.set_caption('Checkers')
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color(BG_COLOR))
    game_state = GameState()
    running = True
    sq_selected = () # keep track of the last click of the user (tuple)
    playerClicks = [] # keep track of the player's clicks (two tuples)
    ValidMoves = []
    make_more_moves = False
    game_state.getValidMoves() # generate all valid moves
    ValidMoves = game_state.moves
    firstCapture = True

    while running:
        if game_state.CapturePossible() and firstCapture:
            game_state.getFirstCaptureMoves() # generate all valid capture moves
            ValidMoves = game_state.firstCaptureMoves

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse clicks    
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sq_selected == (row, col):
                    sq_selected = () # deselect
                    playerClicks = [] # clear the player clicks
                else:
                    sq_selected = (row, col)
                    playerClicks.append(sq_selected)

                # if there is no capture move possible
                if not game_state.CapturePossible():
                    game_state.getValidMoves() # generate all valid moves
                    ValidMoves = game_state.moves
                    if len(playerClicks) == 2:
                        move = Move(playerClicks[0], playerClicks[1], game_state.board)
                        for valid_move in ValidMoves:
                            if valid_move == move:
                                game_state.makeMove(valid_move)
                                game_state.moves = [] # reset moves after making a move
                                game_state.whitesTurn = not game_state.whitesTurn
                                sq_selected = () # reset selected square
                                playerClicks = [] # reset player clicks
                                break
                            else:
                                playerClicks = [sq_selected] 

                # if there is any capture move possible
                elif game_state.CapturePossible():
                    game_state.getFirstCaptureMoves() # generate all valid capture moves
                    ValidMoves = game_state.firstCaptureMoves
                    if len(playerClicks) == 2:
                        move = Move(playerClicks[0], playerClicks[1], game_state.board)
                        if move not in ValidMoves:
                            playerClicks = [sq_selected]
                        else:
                            for valid_move in ValidMoves:
                                if valid_move == move: # if the first capture was made
                                    firstCapture = False
                                    game_state.makeMove(valid_move)
                                    game_state.firstCaptureMoves = [] # reset moves after making a move
                                    sq_selected = () # deselect
                                    playerClicks = [] # clear the player clicks
                                    make_more_moves = moreCapturesAvalible(game_state.board, move.endRow, move.endCol, game_state)
                                    if not make_more_moves: # if there are no more captures for moved pawn
                                        sq_selected = () # deselect
                                        playerClicks = [] # clear the player clicks
                                        game_state.whitesTurn = not game_state.whitesTurn
                                        game_state.nextCaptureMoves = [] # reset moves after making a move
                                        game_state.moveLog[-1].lastCapture = True # set the flag of the last capture move
                                        firstCapture = True
                                    else: # if there are more captures
                                        playerClicks = [(move.endRow, move.endCol)]
                                        sq_selected = (move.endRow, move.endCol) # set selection to the last moved pawn
                                        getMoreCaptures(game_state.board, move.endRow, move.endCol, game_state)
                                        ValidMoves = game_state.nextCaptureMoves
                                        if len(playerClicks) == 2:
                                            move = Move(playerClicks[0], playerClicks[1], game_state.board)
                                            if move in ValidMoves:
                                                for valid_move in ValidMoves:
                                                    if valid_move == move: # if next capture was made
                                                        game_state.makeMove(valid_move)
                                                        make_more_moves = moreCapturesAvalible(game_state.board, move.endRow, move.endCol, game_state)
                                                        game_state.nextCaptureMoves = [] # reset moves after making a move
                                                        sq_selected = () # deselect
                                                        playerClicks = [] # clear the player clicks
                                            else:
                                                playerClicks = [sq_selected]

            
                                    break
            # key clicks
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo button
                    game_state.undoMove()
                    sq_selected = ()
                    playerClicks = []

        updateBoard(screen, game_state, FPS, clock, ValidMoves, sq_selected)


if __name__ == '__main__':
    main()
