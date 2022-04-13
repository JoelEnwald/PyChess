import numpy as np

BROWS = 6
BCOLS = 6

MINWHITEPIECE = 1
MAXWHITEPIECE = 6
MINBLACKPIECE = 7
MAXBLACKPIECE = 12

EMPTY = 0
WKING = 1
WQUEEN = 2
WROOK = 3
WBISHOP = 4
WKNIGHT = 5
WPAWN = 6
BKING = 7
BQUEEN = 8
BROOK = 9
BBISHOP = 10
BKNIGHT = 11
BPAWN = 12

# Allowed movement vectors
NX = [-2, -2, -1, -1, 1, 1, 2, 2]
NY = [1, -1, 2, -2, 2, -2, 1, -1]
BX = [[1,2,3,4,5,6,7],
      [1,2,3,4,5,6,7],
      [-1,-2,-3,-4,-5,-6,-7],
      [-1,-2,-3,-4,-5,-6,-7]]
BY = [[1,2,3,4,5,6,7],
      [-1,-2,-3,-4,-5,-6,-7],
      [1,2,3,4,5,6,7],
      [-1,-2,-3,-4,-5,-6,-7]]
RX = [[0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0],
      [1,2,3,4,5,6,7],
      [-1,-2,-3,-4,-5,-6,-7]]
RY = [[1,2,3,4,5,6,7],
      [-1,-2,-3,-4,-5,-6,-7],
      [0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0]]
KX = [1,1,1,0,0,-1,-1,-1]
KY = [1,0,-1,1,-1,1,0,-1]

class Position(object):

    def __init__(self):
        self.board = np.zeros((BROWS, BCOLS), dtype=int)
        self.whiteToMove = True
        self.cachedResult = None
        self.winner = 0  # white = +1, black = -1

    def setStartingPosition(self):
        for x in range(0, BCOLS):
            self.board[x][1] = WPAWN
            self.board[x][BROWS - 2] = BPAWN
            if (x == 0 or x == BCOLS - 1):
                self.board[x][0] = WROOK
                self.board[x][BROWS - 1] = BROOK
            elif (x == 1 or x == BCOLS - 2):
                self.board[x][0] = WKNIGHT
                self.board[x][BROWS - 1] = BKNIGHT
            elif (BCOLS == 8 and (x == 2 or x == BCOLS - 3)):
                self.board[x][0] == WBISHOP
                self.board[x][BROWS - 1] = BBISHOP
            elif ((BCOLS == 8 and x == 3) or (BCOLS == 6 and x == 2)):
                self.board[x][0] = WQUEEN
                self.board[x][BROWS - 1] = BQUEEN
            elif (x == BCOLS / 2):
                self.board[x][0] = WKING
                self.board[x][BROWS - 1] = BKING

    def cloneEssentialsFrom(self, position):
        for i in range(0, len(self.board)):
            for j in range(len(self.board[i])):
                self.board[i][j] = position.board[i][j]
        self.whiteToMove = not position.whiteToMove

    def countPieces(self):
        amount = 0
        for i in range(0, BROWS):
            for j in range(0, BCOLS):
                if (self.board[i][j] != 0):
                    amount += 1
        return amount

    # Changes black pieces to white and vice versa?
    # Also switches turn
    def mirror(self):
        p = Position()
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[i])):
                piece = self.board[i][BCOLS - 1 - j]
                if (piece != 0):
                    p.board[i][j] = (-6 if piece >= 7 else 6) + piece

        p.whiteToMove = not self.whiteToMove
        return p

    def print(self):
        for y in range(BROWS - 1, -1, -1):
            for x in range(0, BCOLS):
                v = self.board[x][y]
                if (v == EMPTY):
                    print(".", end='')
                if (v == WKING):
                    print("k", end='')
                if (v == WQUEEN):
                    print("q", end='')
                if (v == WROOK):
                    print("r", end='')
                if (v == WBISHOP):
                    print("b", end='')
                if (v == WKNIGHT):
                    print("n", end='')
                if (v == WPAWN):
                    print("p", end='')
                if (v == BKING):
                    print("K", end='')
                if (v == BQUEEN):
                    print("Q", end='')
                if (v == BROOK):
                    print("R", end='')
                if (v == BBISHOP):
                    print("B", end='')
                if (v == BKNIGHT):
                    print("N", end='')
                if (v == BPAWN):
                    print("P", end='')
            print("")

    def isValidPosition(self, p):
        return True

    def isWhitePiece(self, pval):
        if (pval == 0):
            return False
        if (pval < 7):
            return True
        return False

    def isBlackPiece(self, pval):
        if (pval == 0):
            return False
        if (pval > 6):
            return True
        return False

    def isInsideBoard(self, x, y):
        if (x < 0 or x >= BCOLS):
            return False
        if (y < 0 or y >= BROWS):
            return False
        return True

    def squaresContainSameColoredPieces(self, x, y, x2, y2):
        if (self.isWhitePiece(self.board[x][y]) and self.isWhitePiece(self.board[x2][y2])):
            return True
        if (self.isBlackPiece(self.board[x][y]) and self.isBlackPiece(self.board[x2][y2])):
            return True
        return False

    def checkWin(self, x, y):
        # This is a piece just about to be captured.
        # If white king, black wins, and vice versa
        if (self.board[x][y] == WKING):
            return -1
        if (self.board[x][y] == BKING):
            return 1
        return 0

    def getNextPositions(self):
        ret = []

        for x in range(0, len(self.board)):
            for y in range(0, len(self.board)):
                pval = self.board[x][y]

                if (pval == EMPTY):
                    continue
                if (self.whiteToMove != self.isWhitePiece(pval)):
                    continue

                ### PIECE SPECIFIC STUFF ###
                if (pval == WKING or pval == BKING):
                    for i in range(0, len(KX)):
                        x2 = KX[i] + x
                        y2 = KY[i] + y
                        if (not self.isInsideBoard(x2, y2)):
                            continue
                        if (self.squaresContainSameColoredPieces(x, y, x2, y2)):
                            continue
                        p = Position()
                        p.cloneEssentialsFrom(self)
                        p.winner = self.checkWin(x2, y2)
                        p.board[x2][y2] = self.board[x][y]
                        p.board[x][y] = EMPTY
                        ret.append(p)
                    continue

                if (pval == WQUEEN or pval == BQUEEN):
                    # Queens can move like bishops:
                    for i in range(0, len(BX)):
                        # For all the directions
                        for j in range(0, len(BX[i])):
                            # Once a direction is obstructed, finish!
                            x2 = BX[i][j] + x
                            y2 = BY[i][j] + y
                            if (not self.isInsideBoard(x2, y2)):
                                break
                            if (self.squaresContainSameColoredPieces(x, y, x2, y2)):
                                break

                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.winner = self.checkWin(x2, y2)
                            p.board[x2][y2] = self.board[x][y]
                            p.board[x][y] = EMPTY
                            ret.append(p)

                            if (self.board[x2][y2] != EMPTY):
                                # Ate it, and finished direction
                                break

                    # Queens can also move like rooks:
                    for i in range(0, len(RX)):
                        # for all the directions
                        for j in range(0, len(RX[i])):
                            # once a direction is obstructed, finish
                            x2 = RX[i][j] + x
                            y2 = RY[i][j] + y
                            if (not self.isInsideBoard(x2, y2)):
                                break
                            if (self.squaresContainSameColoredPieces(x, y, x2, y2)):
                                break

                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.winner = self.checkWin(x2, y2)
                            p.board[x2][y2] = self.board[x][y]
                            p.board[x][y] = EMPTY
                            ret.append(p)

                            if (self.board[x2][y2] != EMPTY):
                                # ate it, and finished direction
                                break
                    continue

                if (pval == WROOK or pval == BROOK):
                    for i in range(0, len(RX)):
                        # for all the directions
                        for j in range(0, len(RX[i])):
                            # once a direction is obstructed, finish
                            x2 = RX[i][j] + x
                            y2 = RY[i][j] + y
                            if (not self.isInsideBoard(x2, y2)):
                                break
                            if (self.squaresContainSameColoredPieces(x, y, x2, y2)):
                                break

                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.winner = self.checkWin(x2, y2)
                            p.board[x2][y2] = self.board[x][y]
                            p.board[x][y] = EMPTY
                            ret.append(p)

                            if (self.board[x2][y2] != EMPTY):
                                # ate it, and finished direction
                                break
                    continue

                if (pval == WBISHOP or pval == BBISHOP):
                    for i in range(0, len(BX)):
                        # For all the directions
                        for j in range(0, len(BX[i])):
                            # Once a direction is obstructed, finish!
                            x2 = BX[i][j] + x
                            y2 = BY[i][j] + y
                            if (not self.isInsideBoard(x2, y2)):
                                break
                            if (self.squaresContainSameColoredPieces(x, y, x2, y2)):
                                break

                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.winner = self.checkWin(x2, y2)
                            p.board[x2][y2] = self.board[x][y]
                            p.board[x][y] = EMPTY
                            ret.append(p)

                            if (self.board[x2][y2] != EMPTY):
                                # Ate it, and finished direction
                                break
                    continue

                if (pval == WKNIGHT or pval == BKNIGHT):
                    for i in range(0, len(NX)):
                        x2 = NX[i] + x
                        y2 = NY[i] + y
                        if (not self.isInsideBoard(x2, y2)):
                            continue
                        if (self.squaresContainSameColoredPieces(x, y, x2, y2)):
                            continue

                        p = Position()
                        p.cloneEssentialsFrom(self)
                        p.winner = self.checkWin(x2, y2)
                        p.board[x2][y2] = self.board[x][y]
                        p.board[x][y] = EMPTY
                        ret.append(p)
                    continue

                if (pval == WPAWN):
                    allowedMoves = [True]*4
                    # 1 step forward
                    allowedMoves[0] = (self.isInsideBoard(x, y+1) and (self.board[x][y+1] == EMPTY))
                    # 2 steps forward (not in Los Alamos chess)
                    allowedMoves[1] = (BROWS == 8 and self.isInsideBoard(x, y+2) and y == 1 and allowedMoves[0] and self.board[x][y+2] == EMPTY)
                    # eat left
                    allowedMoves[2] = self.isInsideBoard(x-1, y+1) and self.isBlackPiece(self.board[x-1, y+1])
                    # eat right
                    allowedMoves[3] = self.isInsideBoard(x+1, y+1) and self.isBlackPiece(self.board[x+1][y+1])

                    if (allowedMoves[0]):
                        if (y + 1 != BROWS - 1):
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.board[x][y + 1] = pval
                            p.board[x][y] = EMPTY
                            ret.append(p)
                        # Pawn promotion
                        else:
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.board[x][y + 1] = WKNIGHT
                            p.board[x][y] = EMPTY
                            ret.append(p)
                            if (BCOLS == 8):
                                p = Position()
                                p.cloneEssentialsFrom(self)
                                p.board[x][y + 1] = WBISHOP
                                p.board[x][y] = EMPTY
                                ret.append(p)
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.board[x][y + 1] = WROOK
                            p.board[x][y] = EMPTY
                            ret.append(p)
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.board[x][y + 1] = WQUEEN
                            p.board[x][y] = EMPTY
                            ret.append(p)

                    if (allowedMoves[1]):
                        p = Position()
                        p.cloneEssentialsFrom(self)
                        p.board[x][y + 2] = pval
                        p.board[x][y] = EMPTY
                        ret.append(p)

                    if (allowedMoves[2]):
                        if (y + 1 != BROWS - 1):
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.winner = self.checkWin(x - 1, y + 1)
                            p.board[x - 1][y + 1] = pval
                            p.board[x][y] = EMPTY
                            ret.append(p)
                        # Pawn promotion
                        else:
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.winner = self.checkWin(x - 1, y + 1)
                            p.board[x - 1][y + 1] = WKNIGHT
                            p.board[x][y] = EMPTY
                            ret.append(p)
                            if (BCOLS == 8):
                                p = Position()
                                p.cloneEssentialsFrom(self)
                                p.winner = self.checkWin(x - 1, y + 1)
                                p.board[x - 1][y + 1] = WBISHOP
                                p.board[x][y] = EMPTY
                                ret.append(p)
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.winner = self.checkWin(x - 1, y + 1)
                            p.board[x - 1][y + 1] = WROOK
                            p.board[x][y] = EMPTY
                            ret.append(p)
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.winner = self.checkWin(x - 1, y + 1)
                            p.board[x - 1][y + 1] = WQUEEN
                            p.board[x][y] = EMPTY
                            ret.append(p)

                    if (allowedMoves[3]):
                        if (y + 1 != BROWS - 1):
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.winner = self.checkWin(x + 1, y + 1)
                            p.board[x + 1][y + 1] = pval
                            p.board[x][y] = EMPTY
                            ret.append(p)
                        # Pawn promotion
                        else:
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.winner = self.checkWin(x + 1, y + 1)
                            p.board[x + 1][y + 1] = WKNIGHT
                            p.board[x][y] = EMPTY
                            ret.append(p)
                            if (BCOLS == 8):
                                p = Position()
                                p.cloneEssentialsFrom(self)
                                p.winner = self.checkWin(x + 1, y + 1)
                                p.board[x + 1][y + 1] = WBISHOP
                                p.board[x][y] = EMPTY
                                ret.append(p)
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.winner = self.checkWin(x + 1, y + 1)
                            p.board[x + 1][y + 1] = WROOK
                            p.board[x][y] = EMPTY
                            ret.append(p)
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.winner = self.checkWin(x + 1, y + 1)
                            p.board[x + 1][y + 1] = WQUEEN
                            p.board[x][y] = EMPTY
                            ret.append(p)
                    continue

                if (pval == BPAWN):
                    allowedMoves = [True] * 4
                    # 1 step forward
                    allowedMoves[0] = (self.isInsideBoard(x, y - 1) and (self.board[x][y - 1] == EMPTY))
                    # 2 steps forward (not in Los Alamos chess)
                    allowedMoves[1] = BROWS == 8 and self.isInsideBoard(x, y - 2) and y == 6 and \
                                      allowedMoves[0] and self.board[x][y - 2] == EMPTY
                    # eat left
                    allowedMoves[2] = self.isInsideBoard(x - 1, y - 1) and self.isWhitePiece(
                        self.board[x - 1, y - 1])
                    # eat right
                    allowedMoves[3] = self.isInsideBoard(x + 1, y - 1) and self.isWhitePiece(
                        self.board[x + 1][y - 1])

                    if (allowedMoves[0]):
                        if (y - 1 != 0):
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.board[x][y - 1] = pval
                            p.board[x][y] = EMPTY
                            ret.append(p)
                        else:
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.board[x][y - 1] = BKNIGHT
                            p.board[x][y] = EMPTY
                            ret.append(p)
                            if (BCOLS == 8):
                                p = Position()
                                p.cloneEssentialsFrom(self)
                                p.board[x][y - 1] = BBISHOP
                                p.board[x][y] = EMPTY
                                ret.append(p)
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.board[x][y - 1] = BROOK
                            p.board[x][y] = EMPTY
                            ret.append(p)
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.board[x][y - 1] = BQUEEN
                            p.board[x][y] = EMPTY
                            ret.append(p)
                    if (allowedMoves[1]):
                        p = Position()
                        p.cloneEssentialsFrom(self)
                        p.board[x][y - 2] = pval
                        p.board[x][y] = EMPTY
                        ret.append(p)
                    if (allowedMoves[2]):
                        if (y - 1 != 0):
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.winner = self.checkWin(x - 1, y - 1)
                            p.board[x - 1][y - 1] = pval
                            p.board[x][y] = EMPTY
                            ret.append(p)
                        else:
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.winner = self.checkWin(x - 1, y - 1)
                            p.board[x - 1][y - 1] = BKNIGHT
                            p.board[x][y] = EMPTY
                            ret.append(p)
                            if (BCOLS == 8):
                                p = Position()
                                p.cloneEssentialsFrom(self)
                                p.winner = self.checkWin(x - 1, y - 1)
                                p.board[x - 1][y - 1] = BBISHOP
                                p.board[x][y] = EMPTY
                                ret.append(p)
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.winner = self.checkWin(x - 1, y - 1)
                            p.board[x - 1][y - 1] = BROOK
                            p.board[x][y] = EMPTY
                            ret.append(p)
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.winner = self.checkWin(x - 1, y - 1)
                            p.board[x - 1][y - 1] = BQUEEN
                            p.board[x][y] = EMPTY
                            ret.append(p)
                    if (allowedMoves[3]):
                        if (y - 1 != 0):
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.winner = self.checkWin(x + 1, y - 1)
                            p.board[x + 1][y - 1] = pval
                            p.board[x][y] = EMPTY
                            ret.append(p)
                        else:
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.winner = self.checkWin(x + 1, y - 1)
                            p.board[x + 1][y - 1] = BKNIGHT
                            p.board[x][y] = EMPTY
                            ret.append(p)
                            if (BCOLS == 8):
                                p = Position()
                                p.cloneEssentialsFrom(self)
                                p.winner = self.checkWin(x + 1, y - 1)
                                p.board[x + 1][y - 1] = BBISHOP
                                p.board[x][y] = EMPTY
                                ret.append(p)
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.winner = self.checkWin(x + 1, y - 1)
                            p.board[x + 1][y - 1] = BROOK
                            p.board[x][y] = EMPTY
                            ret.append(p)
                            p = Position()
                            p.cloneEssentialsFrom(self)
                            p.winner = self.checkWin(x + 1, y - 1)
                            p.board[x + 1][y - 1] = BQUEEN
                            p.board[x][y] = EMPTY
                            ret.append(p)
                    continue
        return ret