'''
This class is responsible for pawns, their class, functions, visuals etc.
'''

import pygame as p

SIZE = 55

black_crown = p.image.load("images/black_crown.png")
white_crown = p.image.load("images/black_crown.png")


class Pawn:
    def __init__(self, color, second_color):
        self.color = color
        self.second_color = second_color
        self.isQueen = False

    def drawPawn(self,win,x,y):
        p.draw.circle(win, self.color, (x, y), SIZE//2, 0)
        p.draw.circle(win,self.second_color, (x,y), SIZE//3, 0)
        if self.isQueen:
            win.blit(white_crown if self.color == 'white' else black_crown, (x, y))


white_pawn = Pawn('white','gray90')
black_pawn = Pawn('black','gray15')

pawn_dict = {'b':black_pawn, 'w':white_pawn}


