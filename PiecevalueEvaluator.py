import random
from PositionHandler import Position
import numpy as np
import matplotlib.pyplot as plt

BROWS = 6
BCOLS = 6
# Also empty
N_PIECES = 13
PIECE_STRINGS = ['EMPTY', 'WKING', 'WQUEEN', 'WROOK', 'WBISHOP', 'WKNIGHT', 'WPAWN', 'BKING', 'BQUEEN', 'BROOK', 'BBISHOP', 'BKNIGHT', 'BPAWN']

# Both players have their own evaluators
class PiecevalueEvaluator():

    def __init__(self, color):
        np.random.seed(1234321)
        # 0 for white, 1 for black
        self.color = color
        # How many boards have appeared in games. Initialize with 2's
        self.boardcounts = 2
        # How many boards have appeared in won games. Initialize with 1's
        self.winboardcounts = 1
        # For weighted averages
        self.gameweight = 1
        # How many times each piece has appeared over all games. Initialize with twos
        self.piececounts = np.ones(N_PIECES)*2
        # How many times each piece has appeared over all won games. Initialize with ones
        self.piecewincounts = np.ones(N_PIECES)
        self.piecevalues = np.zeros(N_PIECES)

    # For result, 1 = win, -1 = loss, 0 = draw
    def update(self, board_states, result):
        # IF result was not a draw
        if result != 0:
            for board_state in board_states:
                for i in range(0, BROWS):
                    for j in range(0, BCOLS):
                        piece = board_state[i,j]
                        # Ignore empty squares, assume they have no effect on probabilities
                        if piece > 0:
                            self.piececounts[piece] += self.gameweight
                            if result == 1:
                                self.piecewincounts[piece] += self.gameweight
                self.boardcounts += self.gameweight
                if result == 1:
                    self.winboardcounts += self.gameweight
            # For each piece, calculate the values so they can be quickly added together in eval-function
            for piece in range(1, N_PIECES):
                self.piecevalues[piece] = np.log(self.piecewincounts[piece]/self.piececounts[piece]) - np.log(self.winboardcounts/self.boardcounts)
        self.gameweight += 1

    # THIS FUNCTION IS CALLED A LOT! Optimize!
    def eval(self, position, player):
        totalvalue = 0
        for i in range(0, BROWS):
            for j in range(0, BCOLS):
                piece = position.board[i,j]
                if piece > 0:
                    totalvalue += self.piecevalues[piece]
        if player == 0:
            return totalvalue
        else:
            return -totalvalue

    def getEvalMatrix(self):
        return self.piecevalues