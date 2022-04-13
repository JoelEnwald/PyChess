from PositionHandler import Position
from LearningEvaluator import LearningEvaluator
from PiecevalueEvaluator import PiecevalueEvaluator
import AdvancedEvaluator
import time
import numpy as np
import cProfile
import matplotlib.pyplot as plt
import random

DEPTH = 2
EPOCHS = 200
BROWS = 6
BCOLS = 6
SHOWBOARD = 0

class TrainingSession(object):

    def __init__(self):
        self.eval_curr = None
        self.eval1 = None
        self.eval2 = None
        self.POSITIONSEXPLORED = 0

    def comparePositions(self, pos, player):
        return self.evaluate(pos, player)

    def evaluate(self, pos, player):
        if pos.cachedResult is not None:
            return pos.cachedResult
        d = 0.0
        d = self.eval_curr.eval(pos, player)
        pos.cachedResult = d
        return d

    def alphabeta(self, pos, depth, alpha, beta, player):
        # 0 tries to maximize, 1 tries to minimize
        if pos.winner == -1:
            return -1e10 - depth
        if pos.winner == 1:
            return 1e10 + depth
        if depth == 0:
            self.POSITIONSEXPLORED += 1
            return self.eval_curr.eval(pos, player)

        P = pos.getNextPositions()
        P.sort(key=lambda pos: self.evaluate(pos, player))
        # Originally this said "if player == 0"
        if player == 0:
            P.reverse()
            for i in range(0, len(P)):
                alpha = max(alpha, self.alphabeta(P[i], depth - 1, alpha, beta, 1))
                if beta <= alpha:
                    break
            return alpha

        for i in range(0, len(P)):
            beta = min(beta, self.alphabeta(P[i], depth - 1, alpha, beta, 0))
            if beta <= alpha:
                break
        return beta

    def minmax(self, pos, depth, player):
        alpha = float(-2e9); beta = float(2e9)
        return self.alphabeta(pos, depth, alpha, beta, player)

    def countPieces(self, board):
        size = board.length
        count = 0
        for i in range(0, size):
            for j in range(0, size):
                if board[i][j] != 0:
                    count += 1
        return count

    def printMatrix(self, matrixToPrint):
        for i in range(0, self.BROWS):
            print(''.join(matrixToPrint[i][:]))
            print("\n")

    def startSession(self):

        game_board_states = None
        gamecounter = 0
        matrixToPrint = None

        # eval1 gets white pieces, eval2 black ones
        #self.eval1 = AdvancedEvaluator
        self.eval1 = LearningEvaluator(color=0)

        #self.eval2 = AdvancedEvaluator
        self.eval2 = PiecevalueEvaluator(color=1)

        eval1_win_counter = 0
        eval2_win_counter = 0
        winratios1to2 = []
        # Loop for games
        while (gamecounter < EPOCHS):
            if gamecounter % 50 == 1:
                print("Wins and losses are", eval1_win_counter, "to", eval2_win_counter)

            # All board states reached in a game, as a list
            game_board_states = []

            print("Game number", gamecounter)

            p = Position()
            p.setStartingPosition()
            # Print the starting position
            if SHOWBOARD:
                p.print()
                print("\n")
            game_board_states.append(p.board)

            ms = int(round(time.time() * 1000))

            turnCounter = 0
            # Loop for turns
            while turnCounter < 100:
                nextPositions = p.getNextPositions()

                if p.winner == 1:
                    print("White won.")
                    self.eval1.update(game_board_states, result= 1)
                    self.eval2.update(game_board_states, result= -1)
                    eval1_win_counter += 1
                    break
                if p.winner == -1:
                    print("Black won.")
                    self.eval1.update(game_board_states, result= -1)
                    self.eval2.update(game_board_states, result= 1)
                    eval2_win_counter += 1
                    break
                if turnCounter == 99:
                    print("It was a draw.")
                    self.eval1.update(game_board_states, result=0)
                    self.eval2.update(game_board_states, result=0)
                    break
                if len(nextPositions) == 0:
                    print("No more available moves.")
                    break
                # If the game has not ended, find next move
                else:
                    decider = random.random()
                    # Pick a random position
                    if decider < 0.1:
                        p = random.choice(nextPositions)
                    # Choose the best position
                    else:
                        bestPosition = Position()
                        if p.whiteToMove:
                            self.eval_curr = self.eval1
                            maxVal = -1e9
                            for i in range(0, len(nextPositions)):
                                val = self.minmax(nextPositions[i], DEPTH, 0)
                                # White tries to maximise
                                if maxVal < val:
                                    bestPosition = nextPositions[i]
                                    maxVal = val
                        else:
                            self.eval_curr = self.eval2
                            minVal = 1e9
                            for i in range(0, len(nextPositions)):
                                val = self.minmax(nextPositions[i], DEPTH, 1)
                                # Black tries to minimise
                                if minVal > val:
                                    bestPosition = nextPositions[i]
                                    minVal = val

                        assert p.whiteToMove != bestPosition.whiteToMove
                        p = bestPosition
                        if SHOWBOARD:
                            p.print()
                            print("\n")
                        game_board_states.append(p.board)

                        turnCounter += 1
            gamecounter += 1
            if gamecounter % 50 == 0:
                winratios1to2.append(eval1_win_counter/eval2_win_counter)
        plt.figure()
        plt.plot(self.eval2.getEvalMatrix(), marker='.', markersize=12)
        plt.figure()
        plt.plot(winratios1to2)
        plt.show()


#cProfile.run('TrainingSession.startSession(TrainingSession())')

session = TrainingSession()
session.startSession()
hallo = 5