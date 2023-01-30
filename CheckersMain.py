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
    ValidMoves = []
    make_more_moves = False

    while running:
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
                if len(playerClicks) == 1 and game_state.board[row][col] != '-':
                    if game_state.whitesTurn and (game_state.board[row][col] == 'w' or game_state.board[row][col] == 'W'):
                        sq_selected = (row, col)
                    elif not game_state.whitesTurn and (game_state.board[row][col] == 'b' or game_state.board[row][col] == 'B'):
                        sq_selected = (row, col)
                if len(playerClicks) == 2:
                    move = Move(playerClicks[0], playerClicks[1], game_state.board)
                    if move in ValidMoves:
                        game_state.makeMove(move)
                        game_state.moves = [] # reset moves after making a move
                        game_state.whitesTurn = not game_state.whitesTurn
                    sq_selected = () # reset selected square
                    playerClicks = [] # reset player clicks

            elif e.type == p.MOUSEBUTTONDOWN and game_state.CapturePossible():
                game_state.getFirstCaptureMoves() # generate all valid capture moves
                ValidMoves = game_state.firstCaptureMoves
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sq_selected == (row, col):
                    sq_selected = () # deselect
                    playerClicks = [] # clear the player clicks
                else:
                    sq_selected = (row, col)
                    playerClicks.append(sq_selected)
                if len(playerClicks) == 1 and game_state.board[row][col] != '-':
                    if game_state.whitesTurn and (game_state.board[row][col] == 'w' or game_state.board[row][col] == 'W'):
                        sq_selected = (row, col)
                    elif not game_state.whitesTurn and (game_state.board[row][col] == 'b' or game_state.board[row][col] == 'B'):
                        sq_selected = (row, col)
                if len(playerClicks) == 2:
                    move = Move(playerClicks[0], playerClicks[1], game_state.board)
                    if move not in ValidMoves:
                        sq_selected = () # reset selected square
                        playerClicks = [] # reset player clicks
                    else:
                        for valid_move in ValidMoves:
                            if valid_move == move:
                                valid_move.isCaptureMove = True
                                game_state.makeMove(valid_move)
                                game_state.firstCaptureMoves = [] # reset moves after making a move
                                sq_selected = () # deselect
                                playerClicks = [] # clear the player clicks
                                make_more_moves = moreCapturesAvalible(game_state.board, move.endRow, move.endCol, game_state)
                                if not make_more_moves:
                                    sq_selected = () # deselect
                                    playerClicks = [] # clear the player clicks
                                    game_state.whitesTurn = not game_state.whitesTurn
                                    game_state.nextCaptureMoves = [] # reset moves after making a move
                                else:
                                    playerClicks = [(move.endRow, move.endCol)]
                                    sq_selected = (move.endRow, move.endCol)
                                    updateBoard(screen, game_state, FPS, clock, ValidMoves, sq_selected)
                                    getMoreCaptures(game_state.board, move.endRow, move.endCol, game_state)
                                    ValidMoves = game_state.nextCaptureMoves
                                    if len(playerClicks) == 2:
                                        move = Move(playerClicks[0], playerClicks[1], game_state.board)
                                        if move in ValidMoves:
                                            for valid_move in ValidMoves:
                                                if valid_move == move:
                                                    valid_move.isCaptureMove = True
                                                    game_state.makeMove(valid_move)
                                                    make_more_moves = moreCapturesAvalible(game_state.board, move.endRow, move.endCol, game_state)
                                                    game_state.nextCaptureMoves = [] # reset moves after making a move
                                                    sq_selected = () # deselect
                                                    playerClicks = [] # clear the player clicks
                                break
        updateBoard(screen, game_state, FPS, clock, ValidMoves, sq_selected)


if __name__ == '__main__':
    main()
