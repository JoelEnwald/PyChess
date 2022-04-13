import random
import numpy as np
from PositionHandler import Position

# Randomness is currently off
MINWHITEPIECE = 1
MAXWHITEPIECE = 6
MINBLACKPIECE = 7
MAXBLACKPIECE = 12

# White has high rows, black low ones
blackBoostTable = [ [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ],
                        [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ],
                        [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ],
                        [ 0.0, 0.0, 0.15, 0.2, 0.2, 0.15, 0.0, 0.0 ],
                        [ 0.0, 0.0, 0.2, 0.3, 0.3, 0.2, 0.0, 0.0 ],
                        [ 0.0, 0.0, 0.15, 0.1, 0.1, 0.15, 0.0, 0.0 ],
                        [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ],
                        [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ] ]
whiteBoostTable = [ [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ],
                    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ],
                    [ 0.0, 0.0, 0.15, 0.1, 0.1, 0.15, 0.0, 0.0 ],
                    [ 0.0, 0.0, 0.2, 0.3, 0.3, 0.2, 0.0, 0.0 ],
                    [ 0.0, 0.0, 0.15, 0.2, 0.2, 0.15, 0.0, 0.0 ],
                    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ],
                    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ],
                    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ] ]

def eval(paramPosition):
    i = 0; j = 0
    # If we are using a 6x6-board, shift the indexes referring to the boost tables by 1,
    # so that the middle part of it will be used
    if len(paramPosition.board) == 6:
        i = 1
        j = 1
    d = 0
    # Add randomness to algorithm
    #d = random.random() - 0.5
    for k in range(0, len(paramPosition.board)):
        for m in range(0, len(paramPosition.board[k])):
            if paramPosition.board[k][m] != 0:
                if paramPosition.board[k][m] == 1:
                    d += 1e9
                elif paramPosition.board[k][m] == 2:
                    d += 9
                elif paramPosition.board[k][m] == 3:
                    d += 5.25
                elif paramPosition.board[k][m] == 4:
                    d += 3.25
                elif paramPosition.board[k][m] == 5:
                    d += 3
                elif paramPosition.board[k][m] == 6:
                    d += 1
                elif paramPosition.board[k][m] == 7:
                    d -= 1e9
                elif paramPosition.board[k][m] == 8:
                    d -= 8.5 - 0.05*m
                elif paramPosition.board[k][m] == 9:
                    d -= 4.75 - 0.05*m
                elif paramPosition.board[k][m] == 10:
                    d -= 2.75 - 0.05*m
                elif paramPosition.board[k][m] == 11:
                    d -= 2.5 - 0.05*m
                elif paramPosition.board[k][m] == 12:
                    d -= 1 - 0.1*m
                # Check which boost table to use, white or black one. Are we looking at a white or black piece?
                if MINWHITEPIECE <= paramPosition.board[k][m] <= MAXWHITEPIECE:
                    d += whiteBoostTable[m + j][k + i]
                elif MINBLACKPIECE <= paramPosition.board[k][m] <= MAXBLACKPIECE:
                    d -= blackBoostTable[m + j][k + i]
    return d

def getEvalMatrix(piece):
    print("Getting the evaluation matrix is not supported yet.")