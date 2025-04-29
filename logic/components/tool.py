class Tool:
    def __init__(self, id, tile_id, single_use, ends_turn, single_tile, requires_empty):
        self.id = id 
        self.tile_id = tile_id # Number placed in board matrix when placing tile. If tool doesn't require placing a tile, set tile_id < 0
        self.single_use = single_use  
        self.ends_turn = ends_turn 
        self.single_tile = single_tile
        self.requires_empty = requires_empty 