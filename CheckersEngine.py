'''
This file is responsible for storing all the information about the current state of the game.
It is also responsible for checking and returning all the valid moves.
'''

class GameState():
    def __init__(self):
        self.board = [
            ['-', 'b', '-', 'b', '-', 'b', '-', 'b'],
            ['b', '-', 'b', '-', 'b', '-', 'b', '-'],
            ['-', 'b', '-', 'b', '-', 'b', '-', 'b'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['w', '-', 'w', '-', 'w', '-', 'w', '-'],
            ['-', 'w', '-', 'w', '-', 'w', '-', 'w'],
            ['w', '-', 'w', '-', 'w', '-', 'w', '-']
        ]