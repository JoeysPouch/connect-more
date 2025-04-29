import sys
sys.path.append(".")
from logic.config import SQUARE_SIZE

class Disc:
    def __init__(self, row, col, players, board_value, background_colour):
        self.row = row
        self.col = col
        self.players = players
        self.colour = (0,0,0)
        self.square_size = SQUARE_SIZE
        self.radius = int(self.square_size/2.5)
        self.board_value = board_value
        self.position = (self.square_size * self.col + int(self.square_size/2), self.square_size * (self.row+1) + int(self.square_size/2))
        self.background_colour = background_colour

    def get_colour(self):
        if self.board_value in (0,4):
            self.colour = self.background_colour
        elif self.board_value == 1:
            self.colour = self.players[0].colour
        elif self.board_value == 2:
            self.colour = self.players[1].colour
        elif self.board_value == 3:
            self.colour = (255 - self.background_colour[0], 255 - self.background_colour[1], 255 - self.background_colour[2])

if __name__ == "__main__":
    print('\n'.join(sys.path))