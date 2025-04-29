import numpy as np
import sys
sys.path.append(".")
from logic.config import ROW_COUNT, COLUMN_COUNT

class Board:
    def __init__(self):
        self.board = np.zeros((ROW_COUNT, COLUMN_COUNT))

    def position_change(self, pos, turn):
        self.board[pos[1]][pos[0]] = turn

    # Checks whether click location is valid for current tool
    def is_valid_location(self, pos, tool): 
        if tool.single_tile:
            if pos[1] < 0:
                return False
            elif tool.requires_empty:
                return self.board[pos[1]][pos[0]] == 0
            else:
                return self.board[pos[1]][pos[0]] != 0
        elif tool.requires_empty:
            return self.board[0][pos[0]] == 0
        else:
            for row in range(ROW_COUNT):
                if self.board[row][pos[0]] != 0:
                    return True
            return False

    # Finds position for user selection
    def get_next_open_row(self, col):
        for row in range(ROW_COUNT - 2, -1, -1):
            if self.board[row][col] != 0:
                return (col, row + 1)
        return (col, 0)

    def flip_board(self):
        self.board = np.flip(self.board, 0)