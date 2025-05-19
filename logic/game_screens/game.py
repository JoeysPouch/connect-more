import pygame
import sys
import random
from copy import deepcopy
sys.path.append(".")
from logic.components.player import Player
from logic.components.board import Board
from logic.components.sounds import Sounds
from logic.components.tool import Tool
from logic.components.animation import Animation
from logic.game_screens.menu import config_variables

ROW_COUNT = config_variables["row_count"]
COLUMN_COUNT = config_variables["column_count"]
SQUARE_SIZE = config_variables["square_size"]
ELIGIBLE_TOOLS = config_variables["eligible_tools"]
NUMBER_TO_WIN = config_variables["number_to_win"]
SETS_TO_WIN = config_variables["sets_to_win"]
BULLET_MODE = config_variables["bullet_mode"]
TOOL_CHANCE = config_variables["tool_chance"]
VISIBLE_TOOLS = config_variables["visible_tools"]
START_GAME = config_variables["start_game"]


# This contains the main game handling and data
class Game:

    def __init__(self):

        pygame.init()

        # Basic Screen Information and Logic
        self.square_size = SQUARE_SIZE
        screen_height = self.square_size * (ROW_COUNT + 1) + 100
        screen_width = self.square_size * (COLUMN_COUNT + 2)
        size = (screen_width, screen_height)
        self.background_colour = (69,255,69)
        self.window = pygame.display.set_mode(size)
        self.position = (screen_width / 2, screen_height / 2)
        self.pieces = 0
        self.clock = pygame.time.Clock()

        # Generate tools
        self.tool_locations = {}

        if len(ELIGIBLE_TOOLS) > 0:
            for row in range(1, ROW_COUNT):
                for col in range(0, COLUMN_COUNT):
                    if random.random() < TOOL_CHANCE * (1 - row / ROW_COUNT):
                        tool_to_add = random.choice(ELIGIBLE_TOOLS)
                        if tool_to_add == 1:
                            self.tool_locations[(col, row)] = Tool(1, 4, True, False, False, True, False)
                        elif tool_to_add == 2:
                            self.tool_locations[(col, row)] = Tool(2, 3, True, True, True, False, False)
                        elif tool_to_add == 3:
                            self.tool_locations[(col, row)] = Tool(3, 1.5, True, True, True, True, False)
                        elif tool_to_add == 4:
                            self.tool_locations[(col, row)] = Tool(4, 0, True, False, False, False, True)

        # Main Game Audio Setup
        if not BULLET_MODE:
            self.audio = {
                'menu': Sounds(True, False, 'menu_music').upload_sound(),
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
        self.player_1 = Player(1, "Player 1", (255, 0, 0), [Tool(0, 1.5, False, True, False, True, False)])
        self.player_2 = Player(2, "Player 2", (255, 255, 0), [Tool(0, 1.5, False, True, False, True, False)])
        self.turn_manager = TurnManager(self.game_board, self.position, self.player_1, self.player_2, self.tool_locations)
        self.event_handler = EventHandler(self)
        self.renderer = Render(self.window, self.square_size, self.background_colour, self.player_1, self.player_2, self.tool_locations, size, self.game_board.board)

        self.game_loop()

    
    def game_loop(self):
        while True:
            self.clock.tick(60)
            self.turn_manager.timers()
            self.event_handler.events()
            if BULLET_MODE:
                if self.turn_manager.current_player.time == 0:
                    self.turn_manager.other_player.won = True
                    self.turn_manager.game_over = True
            self.renderer.render(self.game_board.board, self.turn_manager.current_player, self.position, self.turn_manager.current_player.tools[self.turn_manager.tool_index])

class TurnManager:
    def __init__(self, board, position, player_1, player_2, tool_locations):
        self.game_board = board
        self.position = position
        self.attempt = False
        self.game_over = False
        self.selection = (-1, -1)
        self.players = [player_1, player_2]
        self.current_player = player_1
        self.other_player = player_2 if self.current_player == player_1 else player_1
        self.tool_index = 0
        self.tool_used = False
        self.number_of_turns = 0
        self.remaining_drops = 1
        self.tool_locations = tool_locations
        self.first_move_made = False

    def timers(self):
        if BULLET_MODE:
            if self.first_move_made:
                self.current_player.ticks += 1
                if self.current_player.ticks % 60 == 0:
                    self.current_player.time -= 1
                    self.current_player.time = max(0, self.current_player.time)

    def player_turn(self):
        if not self.game_over:
            if self.attempt:
                self.first_move_made = True
                if self.number_of_turns == 0 and BULLET_MODE:
                    pygame.mixer.music.load(f'./assets/sound/bullet_mode.mp3')
                    pygame.mixer.music.play(-1)
                current_tool = self.current_player.tools[self.tool_index]
                if self.game_board.is_valid_location(self.selection, current_tool):
                    self.game_board.flip_board()
                    # Flip for the purposes of calculations, then flip back

                    if current_tool.tile_id >= 0:
                        if current_tool.single_tile:
                            position = (self.selection[0], ROW_COUNT - self.selection[1] - 1)
                        else:
                            position = self.game_board.get_next_open_row(self.selection[0])
                            if not current_tool.requires_empty:
                                position = (position[0], position[1] - 1)
                                if current_tool.id == 4:
                                    held_tile_id = self.game_board.board[position[1]][position[0]]
                                    
                        self.game_board.position_change(position, self.current_player.id if current_tool.tile_id == 1.5 else current_tool.tile_id)
                        if position in self.tool_locations:
                            self.current_player.tools.append(self.tool_locations[position])
                            del self.tool_locations[position]

                    self.game_board.flip_board()

                    # print(self.game_board.board)

                    if current_tool.single_use:
                        del self.current_player.tools[self.tool_index] 
                    
                    self.tool_index = 0

                    if current_tool.id == 4:
                        self.current_player.tools = [Tool(-1, held_tile_id, True, False, False, True, False), Tool(0, 3, True, True,  False, True, False)] + self.current_player.tools

                    if current_tool.tile_id in (1, 1.5, 2):
                        if current_tool.id == -1 and current_tool.tile_id != self.current_player.id:
                            if self.winning_move(self.game_board.board, current_tool.tile_id, (ROW_COUNT - position[1] - 1, position[0])):  
                                self.other_player.won = True    
                                self.game_over = True
                        elif self.winning_move(self.game_board.board, self.current_player.id, (ROW_COUNT - position[1] - 1, position[0])):  
                            self.current_player.won = True
                            self.game_over = True
                    
                    if current_tool.ends_turn:
                        self.remaining_drops -= 1
                        if self.remaining_drops == 0:
                            self.switch_turn()
                        self.tool_used = False
                    else:
                        self.tool_used = True



    # reads a line of given length on the board from a given position (pos) in the direction of a given vector
    def find_line(self, board, pos, vector, length):
        line = []
        for k in range(length):
            if pos[0] + k * vector[0] < 0 or pos[1] + k * vector[1] < 0:
                return [False]
            if pos[0] + k * vector[0] >= ROW_COUNT or pos[1] + k * vector[1] >= COLUMN_COUNT:
                return [False]
            next_letter = int(board[pos[0] + k * vector[0]][pos[1] + k * vector[1]])
            line.append(next_letter)
        return line
    
    # generates list of positions to put in find_line to read all lines of given length in direction of given vector that contain point (row, column)
    # useful for checking diagonals
    def start_points(self, row, column, vector, length):
        points = []
        for i in range(length):
            points.append((row + i * vector[0], column + i * vector[1]))
        return points

        
    # Checks if the last move created a win
    def winning_move(self, board, turn, last_pos):
        # checks top left to bottom right diagoanals
        for point in self.start_points(last_pos[0], last_pos[1], (-1, -1), NUMBER_TO_WIN):
            line_to_check = self.find_line(board, point, (1, 1), NUMBER_TO_WIN)
            if set(line_to_check) == {turn}:
                return True
        
        # checks horizontal lines
        for column in range(last_pos[1] - NUMBER_TO_WIN + 1, last_pos[1] + 1):
            line_to_check = self.find_line(board, (last_pos[0], column), (0, 1), NUMBER_TO_WIN)
            if set(line_to_check) == {turn}:
                return True
        
        # checks bottom left to top right
        for point in self.start_points(last_pos[0], last_pos[1], (1, -1), NUMBER_TO_WIN):
            line_to_check = self.find_line(board, point, (-1, 1), NUMBER_TO_WIN)
            if set(line_to_check) == {turn}:
                return True

        # checks vertical line
        line_to_check = self.find_line(board, last_pos, (1, 0), NUMBER_TO_WIN)
        if set(line_to_check) == {turn}:
                return True


    def switch_turn(self):  
        self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]
        self.number_of_turns += 1
        if NUMBER_TO_WIN > 4:
            self.remaining_drops = 2
        else:
            self.remaining_drops = 1

# For event handling and keyboard/mouse logic
class EventHandler:
    def __init__(self, game):
        self.game = game

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.clicks()
            if event.type == pygame.MOUSEMOTION:
                self.mouse_movement(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.game.turn_manager.tool_used:
                self.switch_tool(self.game.turn_manager.tool_index)

        if not BULLET_MODE:
            for layer in ['layer_2', 'layer_3', 'layer_4', 'layer_5', 'layer_6']:
                if self.game.audio[layer].increasing:
                    self.game.audio[layer].increase_volume(0.0005)

    def clicks(self):
        if not self.game.turn_manager.game_over and not self.game.renderer.paused:
            self.game.turn_manager.attempt = True
            self.game.turn_manager.selection = (int(self.game.position[0] / self.game.square_size) - 1, int(self.game.position[1] / self.game.square_size) - 1)
            self.game.turn_manager.player_turn()
            if not BULLET_MODE:
                self.game.audio['piece'].start()
                self.music()
            self.game.attempt = False

    def mouse_movement(self, event):
        if not self.game.turn_manager.game_over:
            self.game.position = (
                min(max(event.pos[0], SQUARE_SIZE * 1.5), SQUARE_SIZE * (COLUMN_COUNT + 0.5)),
                min(max(event.pos[1], SQUARE_SIZE * 1.5), SQUARE_SIZE * (ROW_COUNT + 0.5))
            )


    def music(self):
        thresholds = {
            4: ['layer_2', 'layer_3'],
            10: ['layer_4', 'layer_5'],
            20: ['layer_6']
        }

        for threshold, layers in thresholds.items():
            if self.game.turn_manager.number_of_turns >= threshold:
                for layer in layers:
                    if layer not in self.game.active_layers:
                        if self.game.audio[layer].variable_volume < 1:
                            self.game.audio[layer].increasing = True
                        else:
                            self.game.audio[layer].increasing = False
                        self.game.active_layers.add(layer)

    def switch_tool(self, tool_index):
        if not self.game.turn_manager.game_over:
            self.game.turn_manager.tool_index = (tool_index + 1) % len(self.game.turn_manager.current_player.tools)

# For rendering and graphical type things
class Render:
    def __init__(self, window, square_size, background_colour, player_1, player_2, tool_locations, size, board):
        self.window = window
        self.square_size = square_size
        self.disc_size = int(self.square_size / 2.5)
        self.background_colour = background_colour
        self.players = [player_1, player_2]
        self.tool_locations = tool_locations
        self.images = {
            "4_mouse_sprite" : pygame.transform.scale(pygame.image.load("./assets/images/magnet.png"), (SQUARE_SIZE * 0.8, SQUARE_SIZE * 0.8))
        }
        self.size = size
        self.animations = []
        self.board = board
        self.paused = False

    def render(self, board, turn, position, tool):
        self.draw_board(board)
        self.draw_animations()
        if not self.paused:
            self.draw_mouse_disc(turn, position, tool)
        if BULLET_MODE:
            self.draw_timer(self.players[0])
            self.draw_timer(self.players[1])
        self.winner(self.players)
        self.final_render()

    def draw_board(self, board):
        self.window.fill(self.background_colour)
        if not self.paused:
            self.board = deepcopy(board)
        pygame.draw.rect(self.window, (0, 0, 255), (self.square_size, self.square_size, self.square_size * COLUMN_COUNT, self.square_size * ROW_COUNT))
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                disc_colour = self.get_colour(self.board[r][c])
                disc_pos = SQUARE_SIZE * (c + 1) + int(SQUARE_SIZE/2), SQUARE_SIZE * (r + 1) + int(SQUARE_SIZE/2)
                pygame.draw.circle(self.window, disc_colour, disc_pos, int(SQUARE_SIZE / 2.5))
                if (c, ROW_COUNT - r - 1) in self.tool_locations and VISIBLE_TOOLS:
                    pygame.draw.circle(self.window, "white", disc_pos, int(SQUARE_SIZE / 7.5))

    def draw_mouse_disc(self, turn, position, tool):      
        if tool.mouse_sprite == False:   
            if tool.single_tile:   
                pygame.draw.circle(self.window, turn.colour if tool.tile_id == 1.5 else self.get_colour(tool.tile_id), position, self.disc_size)
                pygame.draw.circle(self.window, (0,0,0),  position, self.disc_size, max(int(self.disc_size / 20), 1))
            else:
                pygame.draw.circle(self.window, turn.colour if tool.tile_id == 1.5 else self.get_colour(tool.tile_id), (position[0], SQUARE_SIZE / 2), self.disc_size)
                pygame.draw.circle(self.window, (0,0,0),  (position[0], SQUARE_SIZE / 2), self.disc_size, max(int(self.disc_size / 20), 1))
        else:
            if tool.single_tile: 
                self.window.blit(self.images[f"{tool.id}_mouse_sprite"], (position[0] - SQUARE_SIZE / 2, position[1] - SQUARE_SIZE / 2))
            else:
                self.window.blit(self.images[f"{tool.id}_mouse_sprite"], (position[0] - SQUARE_SIZE / 2, SQUARE_SIZE / 10))

    def draw_timer(self, player):
        font = pygame.font.SysFont("arialblack", 20)
        number_text = font.render(f"Player {player.id}: 0:{player.time:02}", True, (255, 255, 255))
        self.window.blit(number_text, (10, 30 * player.id + (self.size[1] - 100)))

    def draw_animations(self):
        for animation in self.animations:
            sprite, pos = animation.get_frame_and_pos()
            if animation.complete:
                del animation
                self.paused = False
            else:
                self.window.blit(sprite, ((pos[0] + 1) * SQUARE_SIZE,  (pos[1] + 1) * SQUARE_SIZE))
                if animation.pause_game:
                    self.paused = True

    def winner(self, players):
        for player in players:
            if player.won:
                pygame.draw.rect(self.window, (255, 255, 255), (self.size[0]/2 - 150, self.size[1] / 2 - 100, 300, 200))
                font = pygame.font.SysFont("arialblack", 30)
                winner_message = font.render(f"Congats your when", True, (255, 100, 255))
                winner_player = font.render(f"player  {player.id}", True, (255, 100, 255))
                self.window.blit(winner_message, (self.size[0] / 2 - 150, self.size[1] / 2 - 100, 300, 200))
                self.window.blit(winner_player, (self.size[0] / 2 - 150, self.size[1] / 2, 300, 200))

    def final_render(self):        
        pygame.display.flip()

    def get_colour(self, tile_id):
        if tile_id in (0,4):
            return self.background_colour
        elif tile_id == 1:
            return self.players[0].colour
        elif tile_id == 2:
            return self.players[1].colour
        elif tile_id == 3:
            return (255 - self.background_colour[0], 255 - self.background_colour[1], 255 - self.background_colour[2])
        else:
            return (0,0,0)

if __name__ == "__main__":
    Game()