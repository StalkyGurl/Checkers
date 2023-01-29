'''
This is the main driver file.
'''

import pygame as p
from CheckersEngine import *
from board import *
from pawns import *


WIDTH = HEIGHT = 600
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
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
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
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
                if len(playerClicks) == 2:
                    move = Move(playerClicks[0], playerClicks[1], game_state.board)
                    game_state.makeMove(move)
                    sq_selected = () # reset selected square
                    playerClicks = [] # reset player clicks
                    
        drawGameState(screen,game_state)
        clock.tick(FPS)
        p.display.flip()


if __name__ == '__main__':
    main()
