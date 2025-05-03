class Tool:
    def __init__(self, id, tile_id, single_use, ends_turn, single_tile, requires_empty):
        self.id = id 
        self.tile_id = tile_id # Number placed in board matrix when placing tile. If tool doesn't require placing a tile, set tile_id < 0
        self.single_use = single_use # If true, tool is deleted from inventory after use 
        self.ends_turn = ends_turn # If false, turn doesn't end but only default tool can be used after another tool
        self.single_tile = single_tile # If true, tool affects a single tile rather than a column
        self.requires_empty = requires_empty  # If true, tool can only be played in empty spot. If false, tool cannot be played in empty spot

    def check_surrounding_tiles(self, pos, board):
        for row in range(max(0, pos[1] - 1), min(len(board), pos[1] + 2)):
            for col in range(max(0, pos[0] - 1), min(len(board[0]), pos[0] + 2)): # this is assuming a rectangular board
                if board[row][col] not in (0,4):
                    return False
        return board[pos[1]][pos[0]] == 0