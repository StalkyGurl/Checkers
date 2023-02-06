'''
This is the main driver file.
'''

import pygame as p
import os
from CheckersEngine import *
from AI_Module import *
from board import *
from pawns import *
from buttons import *

FPS = 60

PLAYER_ONE = True # player plays as white
PLAYER_TWO = True # player plays as black
p.init()
p.mixer.init()
p.display.set_caption('Checkers')
screen = p.display.set_mode((WIDTH,HEIGHT))
clock = p.time.Clock()
screen.fill(p.Color(BG_COLOR))
p.mixer.music.load("sounds/bg_music.mp3")
p.mixer.music.play(-1, 0.0)
p.mixer.music.set_volume(0.05)

'''
Main menu screen.
'''
def main_menu():
    global PLAYER_ONE, PLAYER_TWO
    bg = p.image.load("images/bg.png")
    running = True
    while running:
        screen.blit(bg, (0, 0))
        MENU_MOUSE_POS = p.mouse.get_pos()
        MENU_TEXT = get_font(65).render("CHECKERS", True, "#004346")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH//2, 65))

        PVP_BUTTON = Button(image=p.image.load("images/player-vs-player.png"), pos=(WIDTH//2, 170), 
                            text_input="PLAYER VS PLAYER", font=get_font(25), base_color="#2A9D8F", hovering_color="#E5E7E6")
        PVE_BUTTON = Button(image=p.image.load("images/player_vs_AI.png"), pos=(WIDTH//2, 290), 
                            text_input="PLAY VS AI AS WHITE", font=get_font(25), base_color="#2A9D8F", hovering_color="#E5E7E6")
        EVP_BUTTON = Button(image=p.image.load("images/AI_vs_player.png"), pos=(WIDTH//2, 410), 
                            text_input="PLAY VS AI AS BLACK", font=get_font(25), base_color="#2A9D8F", hovering_color="#E5E7E6")
        QUIT_BUTTON = Button(image=p.image.load("images/quit.png"), pos=(WIDTH//2, 530), 
                            text_input="QUIT", font=get_font(30), base_color="#2A9D8F", hovering_color="#E5E7E6")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PVP_BUTTON, PVE_BUTTON, EVP_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                running = False
            if event.type == p.MOUSEBUTTONDOWN:
                if PVP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    PLAYER_ONE = True
                    PLAYER_TWO = True 
                    play()
                if PVE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    PLAYER_ONE = True
                    PLAYER_TWO = False 
                    play()
                if EVP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    PLAYER_ONE = False
                    PLAYER_TWO = True
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    p.quit()
                    running = False

        p.display.update()



'''
The main driver of the code for user input and updating the graphics.
'''
def play():
    screen.fill(p.Color(BG_COLOR))
    pawnSound = p.mixer.Sound(os.path.join('sounds', 'pawn.ogg'))
    captureSound = p.mixer.Sound(os.path.join('sounds', 'pick.ogg'))
    game_state = GameState()
    running = True
    sq_selected = () # keep track of the last click of the user (tuple)
    playerClicks = [] # keep track of the player's clicks (two tuples)
    ValidMoves = []
    make_more_moves = False
    game_state.getValidMoves() # generate all valid moves
    ValidMoves = game_state.moves
    firstCapture = True
    animate = False
    endgame = False

    while running: 

        humanTurn = (game_state.whitesTurn and PLAYER_ONE) or (not game_state.whitesTurn and PLAYER_TWO)

        if game_state.CapturePossible() and firstCapture:
            game_state.getFirstCaptureMoves() # generate all valid capture moves
            ValidMoves = game_state.moves

        elif not game_state.CapturePossible():
            game_state.getValidMoves() # generate all valid moves
            ValidMoves = game_state.moves

        if len(ValidMoves) == 0: # if there are no moves, end the game
            if game_state.whitesTurn: game_state.blackWon = True
            else: game_state.whiteWon = True
            endgame = True

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse clicks    
            elif e.type == p.MOUSEBUTTONDOWN and not game_state.whiteWon and not game_state.blackWon and not animate:
                # human's turn
                if humanTurn:
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
                        if len(playerClicks) == 2:
                            move = Move(playerClicks[0], playerClicks[1], game_state.board)
                            for valid_move in ValidMoves:
                                if valid_move == move:
                                    game_state.makeMove(valid_move)
                                    animate = True
                                    animateMove(valid_move, screen, game_state, clock)
                                    pawnSound.play()
                                    animate = False
                                    game_state.moves = [] # reset moves after making a move
                                    game_state.whitesTurn = not game_state.whitesTurn
                                    sq_selected = () # reset selected square
                                    playerClicks = [] # reset player clicks
                                    break
                                else:
                                    playerClicks = [sq_selected] 

                    # if there is any capture move possible
                    elif game_state.CapturePossible():
                        if firstCapture:
                            game_state.getFirstCaptureMoves() # generate all valid capture moves
                        ValidMoves = game_state.moves
                        if len(playerClicks) == 2:
                            move = Move(playerClicks[0], playerClicks[1], game_state.board)
                            if move not in ValidMoves:
                                playerClicks = [sq_selected]
                            else:
                                for valid_move in ValidMoves:
                                    if valid_move == move: # if the first capture was made
                                        firstCapture = False
                                        game_state.makeMove(valid_move)
                                        animate = True
                                        captureSound.play()
                                        animateMove(valid_move, screen, game_state, clock)
                                        pawnSound.play()
                                        animate = False
                                        game_state.moves = [] # reset moves after making a move
                                        sq_selected = () # deselect
                                        playerClicks = [] # clear the player clicks
                                        make_more_moves = moreCapturesAvalible(game_state.board, move.endRow, move.endCol, game_state)
                                        if not make_more_moves: # if there are no more captures for moved pawn
                                            sq_selected = () # deselect
                                            playerClicks = [] # clear the player clicks
                                            game_state.whitesTurn = not game_state.whitesTurn
                                            game_state.moves = [] # reset moves after making a move
                                            game_state.moveLog[-1].lastCapture = True # set the flag of the last capture move
                                            firstCapture = True
                                        else: # if there are more captures
                                            game_state.moves = []
                                            playerClicks = [(move.endRow, move.endCol)]
                                            sq_selected = (move.endRow, move.endCol) # set selection to the last moved pawn
                                            getMoreCaptures(game_state.board, move.endRow, move.endCol, game_state)
                                            ValidMoves = game_state.moves
                                            if len(playerClicks) == 2:
                                                move = Move(playerClicks[0], playerClicks[1], game_state.board)
                                                if move in ValidMoves:
                                                    for valid_move in ValidMoves:
                                                        if valid_move == move: # if next capture was made
                                                            game_state.makeMove(valid_move)
                                                            animate = True
                                                            captureSound.play()
                                                            animateMove(valid_move, screen, game_state, clock)
                                                            pawnSound.play()
                                                            animate = False
                                                            make_more_moves = moreCapturesAvalible(game_state.board, move.endRow, move.endCol, game_state)
                                                            game_state.moves = [] # reset moves after making a move
                                                            sq_selected = () # deselect
                                                            playerClicks = [] # clear the player clicks
                                                else:
                                                    playerClicks = [sq_selected]
                                        break

            # AI's turn
            elif not humanTurn and not endgame and not animate:
                AIStartedCapturing = False
                if not game_state.CapturePossible() and not AIStartedCapturing:
                    AImove = AIMove(game_state)
                    game_state.makeMove(AImove)
                    animate = True
                    animateMove(AImove, screen, game_state, clock)
                    pawnSound.play()
                    animate = False
                    game_state.moves = [] # reset moves after making a move
                    game_state.whitesTurn = not game_state.whitesTurn
                    humanTurn = (game_state.whitesTurn and PLAYER_ONE) or (not game_state.whitesTurn and PLAYER_TWO)
                # if there is any capture move possible
                elif game_state.CapturePossible():
                    AIStartedCapturing = True
                    if firstCapture:
                        AImove = AIMove(game_state, capturePossible=True, firstCapture=True)
                    game_state.makeMove(AImove)
                    animate = True
                    captureSound.play()
                    animateMove(AImove, screen, game_state, clock)
                    pawnSound.play()
                    animate = False
                    make_more_moves = moreCapturesAvalible(game_state.board, AImove.endRow, AImove.endCol, game_state)
                    game_state.moves = []
                    if not make_more_moves: # if there are no more captures for moved pawn
                        game_state.whitesTurn = not game_state.whitesTurn
                        game_state.moves = [] # reset moves after making a move
                        game_state.moveLog[-1].lastCapture = True # set the flag of the last capture move
                        firstCapture = True
                        humanTurn = (game_state.whitesTurn and PLAYER_ONE) or (not game_state.whitesTurn and PLAYER_TWO)
                    elif make_more_moves:
                        game_state.moves = []
                        getMoreCaptures(game_state.board, AImove.endRow, AImove.endCol, game_state)
                        AImove = AIMove(game_state, capturePossible=True, firstCapture=False)
                        game_state.makeMove(AImove)
                        animate = True
                        captureSound.play()
                        animateMove(AImove, screen, game_state, clock)
                        pawnSound.play()
                        animate = False
                        make_more_moves = moreCapturesAvalible(game_state.board, AImove.endRow, AImove.endCol, game_state)
                        game_state.moves = []
                        humanTurn = (game_state.whitesTurn and PLAYER_ONE) or (not game_state.whitesTurn and PLAYER_TWO) 
                        if not make_more_moves:
                            game_state.whitesTurn = not game_state.whitesTurn
                            game_state.moves = [] # reset moves after making a move
                            game_state.moveLog[-1].lastCapture = True # set the flag of the last capture move
                            firstCapture = True
                            humanTurn = (game_state.whitesTurn and PLAYER_ONE) or (not game_state.whitesTurn and PLAYER_TWO)


            # key clicks
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z and PLAYER_ONE and PLAYER_TWO: # undo button
                    game_state.undoMove()
                    sq_selected = ()
                    playerClicks = []
                elif e.key == p.K_r: # undo button
                    game_state.restartGame()
                    sq_selected = ()
                    playerClicks = []
                    endgame = False
   
        updateBoard(screen, game_state, FPS, clock, ValidMoves, sq_selected)


if __name__ == '__main__':
    main_menu()
