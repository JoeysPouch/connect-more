import sys
sys.path.append("C:\\Users\\Zarrin Rahman\\Documents\\Personal\\coding_adventures\\connect_4\\connect-more")
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
        if self.board_value == 0:
            self.colour = self.background_colour
        elif self.board_value == 1:
            self.colour = self.players[0].colour
        else:
            self.colour = self.players[1].colour

if __name__ == "__main__":
    print('\n'.join(sys.path))