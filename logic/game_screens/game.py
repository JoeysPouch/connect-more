import pygame
import sys
sys.path.append(".")
from logic.components.player import Player
from logic.components.board import Board
from logic.components.disc import Disc
from logic.components.sounds import Sounds
from logic.config import ROW_COUNT, COLUMN_COUNT, SQUARE_SIZE

# This contains the main game handling and data
class Game:

    def __init__(self):

        pygame.init()

        # Basic Screen Information and Logic
        self.square_size = SQUARE_SIZE
        screen_height = self.square_size * (ROW_COUNT + 1)
        screen_width = self.square_size * COLUMN_COUNT
        size = (screen_width, screen_height)
        self.background_colour = (69,255,69)
        self.window = pygame.display.set_mode(size)
        self.position = (0,0)
        self.pieces = 0

        # Main Game Audio Setup
        self.audio = {'menu': Sounds(True, False, 'menu_music').upload_sound(),
                      'layer_1': Sounds(True, False, 'layer_1').upload_sound(),
                      'layer_2': Sounds(True, False, 'layer_2').upload_sound(),
                      'layer_3': Sounds(True, False, 'layer_3').upload_sound(),
                      'layer_4': Sounds(True, False, 'layer_4').upload_sound(),
                      'layer_5': Sounds(True, False, 'layer_5').upload_sound(),
                      'layer_6': Sounds(True, False, 'layer_6').upload_sound(),                    
                      'bomb': Sounds(False, True, 'bomb_sound').upload_sound(),
                      'piece': Sounds(False, True, 'piece_sound').upload_sound(),
                       }

        self.audio['layer_1'].set_volume(1.0)
        self.audio['layer_1'].start(-1, fade_ms = 3000)
        for layer in ['layer_2', 'layer_3', 'layer_4', 'layer_5', 'layer_6']:
            self.audio[layer].start(-1, 0)
            self.audio[layer].set_volume(0.0)
        self.active_layers = set('layer_1')

        # Initialises other classes
        self.game_board = Board()
        self.player_1 = Player(1, "Player 1", (255,0,0), [])
        self.player_2 = Player(2, "Player 2", (255,255,0), [])
        self.turn_manager = TurnManager(self.game_board, self.position, self.player_1, self.player_2)
        self.event_handler = EventHandler(self)
        self.renderer = Render(self.window, self.square_size, self.background_colour, self.player_1, self.player_2)

        self.game_loop()
    
    def game_loop(self):
        while True:
            self.event_handler.events()
            self.renderer.render(self.game_board.board, self.turn_manager.current_player, self.position)


class TurnManager:
    def __init__(self, board, position, player_1, player_2):
        self.game_board = board
        self.position = position
        self.attempt = False
        self.game_over = False
        self.selection = 0
        self.players = [player_1, player_2]
        self.current_player = player_1

    def player_turn(self):
        if not self.game_over:
            if self.attempt:
                if self.game_board.is_valid_location(self.selection):
                    self.game_board.flip_board()
                    # Flip for the purposes of calculations, then flip back
                    position = self.game_board.get_next_open_row(self.selection)
                    self.game_board.position_change(position, self.selection, self.current_player.id)
                    self.game_board.flip_board()
                    # print(self.game_board.board)

                    if self.winning_move(self.game_board.board, self.current_player.id):  
                        self.game_over = True
                    
                    self.switch_turn()

             
    # Checks if the last move created a win. this is an absolute garbage algorithm i stole from youtube
    def winning_move(self, board, turn):
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if board[r][c] == turn and board[r][c+1] == turn and board[r][c+2] == turn and board[r][c+3] == turn:
                    return True

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if board[r][c] == turn and board[r+1][c] == turn and board[r+2][c] == turn and board[r+3][c] == turn:
                    return True

        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if board[r][c] == turn and board[r+1][c+1] == turn and board[r+2][c+2] == turn and board[r+3][c+3] == turn:
                    return True

        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == turn and board[r-1][c+1] == turn and board[r-2][c+2] == turn and board[r-3][c+3] == turn:
                    return True

    def switch_turn(self):  
        self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]



# For event handling and keyboard/mouse logic
class EventHandler:
    def __init__(self, game):
        self.game = game

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.clicks(event)
            if event.type == pygame.MOUSEMOTION:
                self.mouse_movement(event)

        for layer in ['layer_2', 'layer_3', 'layer_4', 'layer_5', 'layer_6']:
            if self.game.audio[layer].increasing:
                self.game.audio[layer].increase_volume(0.0005)

    def clicks(self, event):
        if not self.game.turn_manager.game_over:
            self.game.turn_manager.attempt = True
            self.game.turn_manager.selection = int(event.pos[0]/self.game.square_size)
            self.game.turn_manager.player_turn()
            self.game.audio['piece'].start()
            self.game.pieces += 1
            self.music()
            self.game.attempt = False

    def mouse_movement(self, event):
        if not self.game.turn_manager.game_over:
            self.game.position = event.pos

    def music(self):
        thresholds = {
                    4: ['layer_2', 'layer_3'],
                      10: ['layer_4', 'layer_5'],
                      20: ['layer_6']}
        for threshold, layers in thresholds.items():
            if self.game.pieces >= threshold:
                for layer in layers:
                    if layer not in self.game.active_layers:
                        if self.game.audio[layer].variable_volume < 1:
                            self.game.audio[layer].increasing = True
                        else:
                            self.game.audio[layer].increasing = False
                        self.game.active_layers.add(layer)


# For rendering and graphical type things
class Render:
    def __init__(self, window, square_size, background_colour, player_1, player_2):
        self.window = window
        self.square_size = square_size
        self.disc_size = int(self.square_size / 2.5)
        self.background_colour = background_colour
        self.players = [player_1, player_2]


    def render(self, board, turn, position):
        self.draw_board(board, turn, position)
        self.draw_mouse_disc(turn, position)
        self.final_render()

    def draw_board(self, board, turn, position):
        self.window.fill(self.background_colour)
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(self.window, (0, 0, 255), (self.square_size * c, self.square_size * (r+1), self.square_size, self.square_size))
                self.placed_disc = Disc(r, c, self.players, board[r][c], self.background_colour)
                self.placed_disc.get_colour()
                pygame.draw.circle(self.window, self.placed_disc.colour, self.placed_disc.position, self.placed_disc.radius)

    def draw_mouse_disc(self, turn, position):           
        pygame.draw.circle(self.window, turn.colour, (position[0], SQUARE_SIZE/2), self.disc_size)
        pygame.draw.circle(self.window, (0,0,0),  (position[0], SQUARE_SIZE/2), self.disc_size, max(int(self.disc_size/20), 1))

        
    def final_render(self):        
        pygame.display.flip()

if __name__ == "__main__":
    Game()