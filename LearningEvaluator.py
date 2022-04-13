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
class LearningEvaluator():

    def __init__(self, color):
        np.random.seed(1234321)
        # 0 for white, 1 for black
        self.color = color
        # Assume one won and one lost game have been played
        self.wins = 1
        self.games_nondrawn = 2
        # For weighted averages
        self.gameweight = 3
        # Sum of all turns there has been a given number of a piecetype on the board
        # Currently can have 0-6 of a piece type
        # Initialize in such a way that probabilities will be between 0 and 1
        self.pieceamounts_turns_sum = np.ones((N_PIECES+1, 7), dtype=int)*2
        # Same for only winning positions
        self.pieceamounts_turns_sum_wins = np.ones((N_PIECES+1, 7), dtype=int)
        # Total number of turns played
        self.turns_sum = 14
        # Total number of turns in winning games
        self.turns_sum_wins = 7

        p_po = self.pieceamounts_turns_sum/self.turns_sum
        log_p_po = np.log(p_po)
        p_po_win = self.pieceamounts_turns_sum_wins/self.turns_sum_wins
        log_p_po_win = np.log(p_po_win)
        self.pieceamounts_values = log_p_po_win - log_p_po

    def update(self, board_states, result):
        # If the result is not a draw
        if result != 0:
            # Number of games up by one
            self.games_nondrawn += 1
            self.turns_sum += len(board_states)
            if result == 1:
                # Number of wins up by one
                self.wins += 1
                self.turns_sum_wins += len(board_states)
            # Increasing weight so that latter games affect parameters more
            self.gameweight += 1
            # Find out how many turns was there each amount of each piece type on the board? Up to 6
            pieceamounts_turns_game = np.zeros((N_PIECES+1, 7), dtype=int)
            for board_state in board_states:
                pieceamounts_counts_turn = np.zeros(N_PIECES+1, dtype=int)
                for i in range(0, BROWS):
                    for j in range(0, BCOLS):
                        piece_index = board_state[i][j]
                        if piece_index != 0:
                            # Sum together the amounts of piecetypes on this board
                            pieceamounts_counts_turn[int(piece_index)] += 1
                # Keep track of counts of piecetypes over the game
                for p in range(1, N_PIECES+1):
                    pieceamounts_turns_game[p][pieceamounts_counts_turn[p]] += 1

            # Update the pieceamount counting
            self.pieceamounts_turns_sum += pieceamounts_turns_game
            if result == 1:
                self.pieceamounts_turns_sum_wins += pieceamounts_turns_game
            # Probability of there being each amount of each piecetype on a played board
            p_po = self.pieceamounts_turns_sum / self.turns_sum
            log_p_po = np.log(p_po)
            # Probability of there being each amount of each piecetype on won played board
            p_po_win = self.pieceamounts_turns_sum_wins / self.turns_sum_wins
            log_p_po_win = np.log(p_po_win)
            self.pieceamounts_values = log_p_po_win - log_p_po

    # THIS FUNCTION IS CALLED A LOT! Optimize!
    def eval(self, position, player):
        p_win_pieceamounts = 0
        # log(p(win)) is not needed since
        # it will be the same for all positions
        pieceamounts_board = np.zeros(13, dtype=int)
        for i in range(0, BROWS):
            for j in range(0, BCOLS):
                piece_index = position.board[i][j]
                # Ignore empty squares
                if piece_index != 0:
                    pieceamounts_board[piece_index] += 1
        for piece_index in range(1, 13):
            p_win_pieceamounts += self.pieceamounts_values[piece_index, pieceamounts_board[piece_index]]
        if player == 0:
            return p_win_pieceamounts
        else:
            return -p_win_pieceamounts

    def getEvalMatrix(self, piece):
        print("Getting the evaluation matrix is not supported yet.")