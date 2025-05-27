import numpy as np
import sys
sys.path.append(".")
from logic.game_screens.menu import config_variables

ROW_COUNT = config_variables["row_count"]
COLUMN_COUNT = config_variables["column_count"]

class Board:
    def __init__(self):
        self.board = np.zeros((ROW_COUNT, COLUMN_COUNT))
        self.frozen_columns = {}

    def position_change(self, pos, turn):
        self.board[pos[1]][pos[0]] = turn

    # Checks whether click location is valid for current tool
    def is_valid_location(self, pos, tool): 
        if pos[0] in self.frozen_columns:
            return False
        if tool.id == 5:
            return True
        if tool.single_tile:
            if tool.id == 3:
                return tool.check_surrounding_tiles(pos, self.board)
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
        for row in range(ROW_COUNT - 1, -1, -1):
            if self.board[row][col] != 0:
                return (col, row + 1)
        return (col, 0)

    def flip_board(self):
        self.board = np.flip(self.board, 0)