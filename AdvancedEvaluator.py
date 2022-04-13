import random
import numpy as np
from PositionHandler import Position

# Randomness is currently off
MINWHITEPIECE = 1
MAXWHITEPIECE = 6
MINBLACKPIECE = 7
MAXBLACKPIECE = 12

# White has high rows, black low ones
whitePawnBoostTable = np.divide([[0, 0, 0, 0, 0, 0, 0, 0],
                                 [50, 50, 50, 50, 50, 50, 50, 50],
                                 [10, 10, 20, 30, 30, 20, 10, 10],
                                 [5,  5, 10, 25, 25, 10,  5,  5],
                                 [0,  0,  0, 20, 20,  0,  0,  0],
                                 [5, -5,-10,  0,  0,-10, -5,  5],
                                 [5, 10, 10,-20,-20, 10, 10,  5],
                                 [0,  0,  0,  0,  0,  0,  0,  0]], 100)

whiteKnightBoostTable = np.divide([[-50, -40, -30, -30, -30, -30, -40, -50],
                                   [-40,-20,  0,  0,  0,  0,-20,-40],
                                   [-30,  0, 10, 15, 15, 10,  0,-30],
                                   [-30,  5, 15, 20, 20, 15,  5,-30],
                                   [-30,  0, 15, 20, 20, 15,  0,-30],
                                   [-30,  5, 10, 15, 15, 10,  5,-30],
                                   [-40,-20,  0,  5,  5,  0,-20,-40],
                                   [-50,-40,-30,-30,-30,-30,-40,-50]], 100)

whiteBishopBoostTable = np.divide([[-20, -10, -10, -10, -10, -10, -10, -20],
                                   [-10,  0,  0,  0,  0,  0,  0,-10],
                                   [-10,  0,  5, 10, 10,  5,  0,-10],
                                   [-10,  5,  5, 10, 10,  5,  5,-10],
                                   [-10,  0, 10, 10, 10, 10,  0,-10],
                                   [-10, 10, 10, 10, 10, 10, 10,-10],
                                   [-10,  5,  0,  0,  0,  0,  5,-10],
                                   [-20,-10,-10,-10,-10,-10,-10,-20]], 100)

whiteRookBoostTable = np.divide([[0, 0, 0, 0, 0, 0, 0, 0],
                                 [5, 10, 10, 10, 10, 10, 10,  5],
                                 [-5,  0,  0,  0,  0,  0,  0, -5],
                                 [-5,  0,  0,  0,  0,  0,  0, -5],
                                 [-5,  0,  0,  0,  0,  0,  0, -5],
                                 [-5,  0,  0,  0,  0,  0,  0, -5],
                                 [-5,  0,  0,  0,  0,  0,  0, -5],
                                 [0,  0,  0,  5,  5,  0,  0,  0]], 100)

whiteQueenBoostTable = np.divide([[-20, -10, -10, -5, -5, -10, -10, -20],
                                  [-10,  0,  0,  0,  0,  0,  0,-10],
                                  [-10,  0,  5,  5,  5,  5,  0,-10],
                                  [-5,  0,  5,  5,  5,  5,  0, -5],
                                  [0,  0,  5,  5,  5,  5,  0, -5],
                                  [-10,  5,  5,  5,  5,  5,  0,-10],
                                  [-10,  0,  5,  0,  0,  0,  0,-10],
                                  [-20,-10,-10, -5, -5,-10,-10,-20]], 100)

whiteKingBoostTable = np.divide([[-30, -40, -40, -50, -50, -40, -40, -30],
                                 [-30,-40,-40,-50,-50,-40,-40,-30],
                                 [-30,-40,-40,-50,-50,-40,-40,-30],
                                 [-30,-40,-40,-50,-50,-40,-40,-30],
                                 [-20,-30,-30,-40,-40,-30,-30,-20],
                                 [-10,-20,-20,-20,-20,-20,-20,-10],
                                 [20, 20,  0,  0,  0,  0, 20, 20],
                                 [20, 30, 10,  0,  0, 10, 30, 20]], 100)


def eval(paramPosition, player):
    i = 0; j = 0
    # The board is stored at different orientation to the tables. Rotate the board
    board = np.rot90(paramPosition.board)
    board_size = len(board)
    # If we are using a 6x6-board, shift the indices referring to the boost tables by 1,
    # so that the middle part of it will be used
    if board_size == 6:
        i = 1
        j = 1
    d = 0
    # Add randomness to algorithm
    #d = random.random() - 0.5
    # Calculation initially assumes white player. The value of d is switched if the player is black
    for k in range(0, len(board)):
        for m in range(0, len(board[k])):
            x = k+i
            y = m+j
            if board[k][m] != 0:
                # White pieces
                if board[k][m] == 1:
                    d += 1e6 + whiteKingBoostTable[x][y]
                elif board[k][m] == 2:
                    d += 9 + whiteQueenBoostTable[x][y]
                elif board[k][m] == 3:
                    d += 5 + whiteRookBoostTable[x][y]
                elif board[k][m] == 4:
                    d += 3.3 + whiteBishopBoostTable[x][y]
                elif board[k][m] == 5:
                    d += 3.2 + whiteKnightBoostTable[x][y]
                elif board[k][m] == 6:
                    d += 1 + whitePawnBoostTable[x][y]
                # For black pieces, a mirrored board is used
                elif board[k][m] == 7:
                    d -= 1e6 + whiteKingBoostTable[8-x-1][y]
                elif board[k][m] == 8:
                    d -= 9 + whiteQueenBoostTable[8-x-1][y]
                elif board[k][m] == 9:
                    d -= 5 + whiteRookBoostTable[8-x-1][y]
                elif board[k][m] == 10:
                    d -= 3.3 + whiteBishopBoostTable[8-x-1][y]
                elif board[k][m] == 11:
                    d -= 3.2 + whiteKnightBoostTable[8-x-1][y]
                elif board[k][m] == 12:
                    d -= 1 + whitePawnBoostTable[8-x-1][y]
    return d

def getEvalMatrix(piece):
    print("Getting the evaluation matrix is not supported yet.")

# Does nothing
def update(board_states, result):
    hallo = 5
hallo = 5