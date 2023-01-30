'''
This class is responsible for pawns, their class, functions, visuals etc.
'''

import pygame as p

SIZE = 55

black_crown = p.image.load("images/black_crown.png")
white_crown = p.image.load("images/white_crown.png")


class Pawn:
    def __init__(self, color, second_color, isQueen=False):
        self.color = color
        self.second_color = second_color
        self.isQueen = isQueen

    def drawPawn(self,win,x,y):
        p.draw.circle(win, self.color, (x, y), SIZE//2, 0)
        p.draw.circle(win,self.second_color, (x,y), SIZE//3, 0)
        if self.isQueen:
            win.blit(white_crown if self.color == 'black' else black_crown, (x - SIZE//2.75, y - SIZE//2.75))


white_pawn = Pawn('white', 'gray90')
black_pawn = Pawn('black', 'gray15')
white_queen = Pawn('white', 'gray90', isQueen=True)
black_queen = Pawn('black', 'gray15', isQueen=True)

pawn_dict = {'b':black_pawn, 'w':white_pawn, 'B':black_queen, 'W':white_queen}


