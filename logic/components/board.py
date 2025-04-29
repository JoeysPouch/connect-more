import numpy as np
import sys
sys.path.append(".")
from logic.config import ROW_COUNT, COLUMN_COUNT

class Board:
    def __init__(self):
        self.board = np.zeros((ROW_COUNT, COLUMN_COUNT))

    def position_change(self, row, col, turn):
        self.board[row][col] = turn

    # Checks whether top row is taken 
    def is_valid_location(self, col):      
        print(self.board[0][col] == 0)
        return self.board[0][col] == 0

    # Finds position for user selection
    def get_next_open_row(self, col):
        for row in range(ROW_COUNT):
            if self.board[row][col] == 0:
                return row

    def flip_board(self):
        self.board = np.flip(self.board, 0)