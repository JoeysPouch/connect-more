import pygame

config_variables = {
    "row_count": 6,
    "column_count": 6,
    "square_size": 100,
    "eligible_tools": [0],
    "number_to_win": 4,
    "sets_to_win": 1,
    "bullet_mode": False,
    "visible_tools": True,
    "tool_chance": 0.1,
    "start_game": False
}


pygame.init()

big_font = pygame.font.Font("assets/other/pixel_game_font.otf", 50)
small_font = pygame.font.Font("assets/other/pixel_game_font.otf", 35)
tiny_font = pygame.font.Font("assets/other/pixel_game_font.otf", 20)

#big_font = pygame.font.SysFont("arialblack", 35)
#small_font = pygame.font.SysFont("arialblack", 25)
#tiny_font = pygame.font.SysFont("arialblack", 15)
TEXT_COL = (255, 255, 255)
BUTTON_COL = (210, 105, 30)
BACKGROUND_COLOUR = (244,164,96)
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 720
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
window = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.flip()
window.fill(BACKGROUND_COLOUR)


class Button:
    def __init__(self, name, location, status, appearance, tickable, font=big_font):
        self.name = name
        self.location = location
        self.status = status
        self.appearance = appearance
        self.tickable = tickable
        self.dragging = False
        self.is_slider = appearance == "slider"
        self.font = font

    def slider(self, event, rows, columns):
        
        rect = pygame.Rect(self.location)
        if event.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(event.pos):
            self.dragging = True

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            x = event.pos[0] - 15
            if self.name == "Row Slider":
                self.location[0] = max(55, min(x, 245))
                rows = int((self.location[0] - 10) / 7.5)
            else:
                self.location[0] = max(400, min(x, 590))
                columns = int((self.location[0] - 355) / 7.5)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragging:
            self.dragging = False
            
        return rows, columns
    

    
    def action_from_click(self):
        self.status = not self.status

        if self.name == "Title":
            pass
        if self.name == "Connect 4":
            config_variables["number_to_win"] = 4
            connect5_button.status = False
            connect6_button.status = False
        if self.name == "Connect 5":
            config_variables["number_to_win"] = 5
            connect4_button.status = False
            connect6_button.status = False       
        if self.name == "Connect 6":
            config_variables["number_to_win"] = 6
            connect4_button.status = False
            connect5_button.status = False
        if self.name == "Bomb":
            if self.status:
                config_variables["eligible_tools"].append(2)
            else:
                config_variables["eligible_tools"].remove(2)
        if self.name == "Floating Tile":
            if self.status:
                config_variables["eligible_tools"].append(3)
            else:
                config_variables["eligible_tools"].remove(3)
        if self.name == "Magnet":
            if self.status:
                config_variables["eligible_tools"].append(4)
            else:
                config_variables["eligible_tools"].remove(4)
        if self.name == "Freeze":
            if self.status:
                config_variables["eligible_tools"].append(5)
            else:
                config_variables["eligible_tools"].remove(5)
        if self.name == "1 Set":
            config_variables["sets_to_win"] = 1
            set2_button.status = False
            set3_button.status = False
        if self.name == "2 Sets":
            config_variables["sets_to_win"] = 2
            set1_button.status = False
            set3_button.status = False
        if self.name == "3 Sets":
            config_variables["sets_to_win"] = 3
            set1_button.status = False
            set2_button.status = False
        if self.name == "Low Frequency":
            config_variables["tool_chance"] = 0.1
            medium_freq_button.status = False
            high_freq_button.status = False
        if self.name == "Medium Frequency":
            config_variables["tool_chance"] = 0.15
            low_freq_button.status = False
            high_freq_button.status = False
        if self.name == "High Frequency":
            config_variables["tool_chance"] = 0.20
            low_freq_button.status = False
            medium_freq_button.status = False
        if self.name == "Bullet Mode":
            config_variables["bullet_mode"] = not config_variables["bullet_mode"]
        if self.name == "Items Visible":
            config_variables["visible_tools"] = not config_variables["visible_tools"]

        if self.name == "Start":
            config_variables["square_size"] = min(500 / config_variables["row_count"], 1000 / config_variables["column_count"])
            config_variables["start_game"] = True
            print(config_variables)
    

class Info:
    def __init__(self, x, y, width, height, *text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.rect = pygame.Rect(x - 10, y - 10, 20, 20)

    def display(self):
        pygame.draw.circle(window, (120, 52, 25), (self.x, self.y), 10)
        pygame.draw.circle(window, TEXT_COL, (self.x, self.y - 5), 2)
        pygame.draw.line(window, TEXT_COL, (self.x - 1, self.y - 1), (self.x - 1, self.y + 6), 2)

    def on_hover(self):
        x = self.x if self.x + self.width + 3 < SCREEN_WIDTH else self.x - self.width
        y = self.y if self.y + self.height + 3 < SCREEN_HEIGHT else self.y - self.height
        pygame.draw.rect(window, (120, 52, 25), (x, y, self.width, self.height))
        pygame.draw.rect(window, BUTTON_COL, (x - 3, y - 3, self.width + 6, self.height + 6), 3, 5)
        buffer = 5
        for line in self.text:
            draw_text(line, tiny_font, TEXT_COL, x + 10, y + buffer)
            buffer += 18


#Buttons

title_button = Button("Title", [150, 15, 390, 70], True, "      CONNECT MORE", False) # why are you a button?

start_button = Button("Start", [260, 650, 200, 60], False, "    START", False)

bullet_mode = Button("Bullet Mode", [580, 380, 40, 40], False, "", True, small_font)

connect4_button = Button("Connect 4", [50, 380, 40, 40], True, "4", True, small_font)
connect5_button = Button("Connect 5", [115, 380, 40, 40], False, "5", True, small_font)
connect6_button = Button("Connect 6", [180, 380, 40, 40], False, "6", True, small_font)

bomb_button = Button("Bomb", [60, 505, 72, 72], False, f"./assets/images/bomb-sprite.png", True)
floating_tile_button = Button("Floating Tile", [140, 505, 72, 72], False, f"./assets/images/bomb.png", True)
magnet_button = Button("Magnet", [60, 585, 72, 72], False, f"./assets/images/magnet-sprite.png", True)
freeze_button = Button("Freeze", [140, 585, 72, 72], False, f"./assets/images/freeze-sprite.png", True)
visible_tools = Button("Items Visible", [475, 570, 40, 40], True, "", True)

set1_button = Button("1 Set", [275, 380, 40, 40], True, "1", True, small_font)
set2_button = Button("2 Sets", [340, 380, 40, 40], False, "2", True, small_font)
set3_button = Button("3 Sets", [405, 380, 40, 40], False, "3", True, small_font)

low_freq_button = Button("Low Frequency", [475, 500, 40, 40], False, "L", True, small_font)
medium_freq_button = Button("Medium Frequency", [530, 500, 40, 40], False, "M", True, small_font)
high_freq_button = Button("High Frequency", [585, 500, 40, 40], False, "H", True, small_font)

rows_label = Button("Rows", [55, 220, 220, 30], True, None, False)
columns_label = Button("Columns", [400, 220, 220, 30], True, None, False)
row_slider = Button("Row Slider", [55, 210, 30, 50], False, "slider", False)
column_slider = Button("Column Slider", [400, 210, 30, 50], False, "slider", False)

buttons = [
    title_button,
    rows_label,
    columns_label,
    row_slider,
    column_slider,
    connect4_button,
    connect5_button,
    connect6_button,
    set1_button,
    set2_button,
    set3_button,
    bullet_mode,
    bomb_button,
    floating_tile_button,
    magnet_button,
    freeze_button,
    low_freq_button,
    medium_freq_button,
    high_freq_button,
    visible_tools,
    start_button,
]

test_info = Info(680, 351, 160, 75, "Fast-paced mode", "with a 30 second", "chess clock!")
bomb_info = Info(120, 565, 160, 50, "Explode the other", "player's piece!")
magnet_info = Info(120, 645, 180, 75, "Move the other" ,"player's piece and", "replace it with junk!")
floating_info = Info(200, 565, 190, 50, "Place an anti-gravity", "floating tile!")
ice_info = Info(200, 645, 140, 50, "Freeze a column", "for 3 turns!")
infos = [test_info, bomb_info, magnet_info, floating_info, ice_info]

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x,y))

def clicks(event):
    for button in buttons:
        rect = pygame.Rect(button.location)
        if rect.collidepoint(event.pos[0], event.pos[1]):
            button.action_from_click()
            print(button.name)

def run_menu():
    pygame.mixer.music.load(f'./assets/sound/menu_music.wav')
    if not config_variables["start_game"]:
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
    window = pygame.display.set_mode(size, pygame.RESIZABLE)
    pygame.display.flip()
    while True:

        #Render
        window.fill(BACKGROUND_COLOUR)
        for button in buttons:
            pygame.draw.rect(window, BUTTON_COL, button.location)
            pygame.draw.rect(window, (120, 52, 25), (button.location[0] - 3, button.location[1] - 3, button.location[2] + 6, button.location[3] + 6), 3, 5)
            if isinstance(button.appearance, str):
                if button.appearance[-3:] == "png":
                    sprite = pygame.image.load(button.appearance)
                    image = pygame.Surface((48, 48)).convert_alpha()
                    image.fill(BUTTON_COL)
                    image.blit(sprite, (0, 0), (0, 0, 48, 48))
                    image = pygame.transform.scale(image, (72, 72))
                    window.blit(image, (button.location[0], button.location[1]))
                
                elif button.is_slider:
                    pygame.draw.rect(window, (120, 52, 25), (button.location))
                else:
                    draw_text(button.appearance, button.font, TEXT_COL, button.location[0] + 10, button.location[1])

                if button.status and button.tickable:
                    overlay = pygame.Surface((button.location[2], button.location[3]), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 100))
                    window.blit(overlay, (button.location[0], button.location[1]))
                    pygame.draw.line(window, (0, 200, 0), (button.location[0], button.location[1] + button.location[3]/2), (button.location[0] + button.location[2]/3, button.location[1] + button.location[3]), 10)
                    pygame.draw.line(window, (0, 200, 0), (button.location[0] + button.location[2]/3, button.location[1] + button.location[3]), (button.location[0] + button.location[2], button.location[1]), 10)
                

        draw_text("Board Size", big_font, TEXT_COL, 45, 105)
        draw_text(f"Rows: {config_variables['row_count']}", small_font, TEXT_COL, 110, 160)
        draw_text(f"Columns: {config_variables['column_count']}", small_font, TEXT_COL, 430, 160)
        draw_text("Rules", big_font, TEXT_COL, 45, 280)
        draw_text("Connect", small_font, TEXT_COL, 45, 335)
        draw_text("Sets to Win", small_font, TEXT_COL, 275, 335)
        draw_text("Bullet Mode", small_font, TEXT_COL, 500, 335)
        draw_text("Powerups", big_font, TEXT_COL, 45, 440)
        draw_text("Frequency", small_font, TEXT_COL, 315, 500)
        draw_text("Visibility", small_font, TEXT_COL, 325, 570)

        for info in infos:
            info.display()

            if info.rect.collidepoint(pygame.mouse.get_pos()):
                info.on_hover()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            for button in buttons:
                if button.is_slider:
                    config_variables["row_count"], config_variables["column_count"] = button.slider(event, config_variables["row_count"], config_variables["column_count"])

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicks(event)

        if config_variables["start_game"]:
            pygame.mixer.music.fadeout(750)
            return
        
        pygame.display.flip()

def start_game():
    return config_variables["start_game"]

run_menu()

