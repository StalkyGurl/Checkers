'''
This is the main driver file.
'''

import pygame as p
from CheckersEngine import *
from board import *
from pawns import *

FPS = 30

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

    while running:
        moveMade = False
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN and not game_state.CapturePossible():
                game_state.getValidMoves() # generate all valid moves
                ValidMoves = game_state.moves
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sq_selected == (row, col):
                    sq_selected = () # deselect
                    playerClicks = [] # clear the player clicks
                else:
                    sq_selected = (row, col)
                    playerClicks.append(sq_selected)
                if len(playerClicks) == 1 and not moveMade:
                    game_state.getValidMoves() # generate all valid moves
                    ValidMoves = game_state.moves
                elif len(playerClicks) == 2 and not moveMade:
                    move = Move(playerClicks[0], playerClicks[1], game_state.board)
                    if move in ValidMoves:
                        game_state.makeMove(move)
                        game_state.moves = [] # reset moves after making a move
                        moveMade = True
                        game_state.whitesTurn = not game_state.whitesTurn
                    sq_selected = () # reset selected square
                    playerClicks = [] # reset player clicks

            elif e.type == p.MOUSEBUTTONDOWN and game_state.CapturePossible():
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sq_selected == (row, col):
                    sq_selected = () # deselect
                    playerClicks = [] # clear the player clicks
                else:
                    sq_selected = (row, col)
                    playerClicks.append(sq_selected)
                if len(playerClicks) == 1 and not moveMade:
                    game_state.getFirstCaptureMoves() # generate all valid capture moves
                    ValidCaptureMoves = game_state.firstCaptureMoves
                elif len(playerClicks) == 2 and not moveMade:
                    move = Move(playerClicks[0], playerClicks[1], game_state.board)
                    if move not in ValidCaptureMoves:
                        sq_selected = () # reset selected square
                        playerClicks = [] # reset player clicks
                    else:
                        for valid_move in ValidCaptureMoves:
                            if valid_move == move:
                                valid_move.isCaptureMove = True
                                game_state.makeMove(valid_move)
                                game_state.firstCaptureMoves = [] # reset moves after making a move
                                sq_selected = () # deselect
                                playerClicks = [] # clear the player clicks
                                make_more_moves = moreCapturesAvalible(game_state.board, valid_move.endRow, valid_move.endCol, game_state)
                                if make_more_moves:
                                    drawGameState(screen,game_state)
                                    clock.tick(FPS)
                                    p.display.flip()
                                    while make_more_moves:
                                        playerClicks = [(move.endRow, move.endCol)]
                                        getMoreCaptures(game_state.board, move.endRow, move.endCol, game_state)
                                        ValidMoves = game_state.nextCaptureMoves
                                        sq_selected = (row, col)
                                        playerClicks.append(sq_selected)
                                        move = Move(playerClicks[0], playerClicks[1], game_state.board)
                                        for valid_move in ValidMoves:
                                            if valid_move == move:
                                                valid_move.isCaptureMove = True
                                                game_state.makeMove(valid_move)
                                                make_more_moves = moreCapturesAvalible(game_state.board, valid_move.endRow, valid_move.endCol, game_state)
                                                game_state.nextCaptureMoves = [] # reset moves after making a move
                                                sq_selected = () # deselect
                                                playerClicks = [] # clear the player clicks
                                                drawGameState(screen,game_state)
                                                clock.tick(FPS)
                                                p.display.flip()
                                moveMade = True
                                game_state.whitesTurn = not game_state.whitesTurn
        drawGameState(screen,game_state)
        clock.tick(FPS)
        p.display.flip()


if __name__ == '__main__':
    main()
