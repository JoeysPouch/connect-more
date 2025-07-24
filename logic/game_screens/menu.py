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

big_font = pygame.font.SysFont("arialblack", 35)
small_font = pygame.font.SysFont("arialblack", 25)
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
    def __init__(self, name, location, status, appearance, tickable):
        self.name = name
        self.location = location
        self.status = status
        self.appearance = appearance
        self.tickable = tickable
        self.dragging = False
        self.is_slider = appearance == "slider"

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


#Buttons

title_button = Button("Title", [150, 15, 390, 70], True, "CONNECT MORE", False) # why are you a button?

start_button = Button("Start", [260, 600, 200, 60], False, " START", False)

bullet_mode = Button("Bullet Mode", [640, 100, 60, 60], False, "", True)

connect4_button = Button("Connect 4", [50, 250, 60, 60], True, "4", True)
connect5_button = Button("Connect 5", [130, 250, 60, 60], False, "5", True)
connect6_button = Button("Connect 6", [210, 250, 60, 60], False, "6", True)

bomb_button = Button("Bomb", [50, 400, 60, 60], False, f"./assets/images/bomb.png", True)
floating_tile_button = Button("Floating Tile", [130, 400, 60, 60], False, f"./assets/images/bomb.png", True)
magnet_button = Button("Magnet", [210, 400, 60, 60], False, f"./assets/images/bomb.png", True)
freeze_button = Button("Freeze", [290, 330, 60, 60], False, f"./assets/images/freeze.png", True)
visible_tools = Button("Items Visible", [290, 400, 60, 60], True, "", True)

set1_button = Button("1 Set", [450, 250, 60, 60], True, "1", True)
set2_button = Button("2 Sets", [530, 250, 60, 60], False, "2", True)
set3_button = Button("3 Sets", [610, 250, 60, 60], False, "3", True)

low_freq_button = Button("Low Frequency", [450, 400, 60, 60], False, "L", True)
medium_freq_button = Button("Medium Frequency", [530, 400, 60, 60], False, "M", True)
high_freq_button = Button("High Frequency", [610, 400, 60, 60], False, "H", True)

rows_label = Button("Rows", [55, 240, 220, 40], True, None, False)
columns_label = Button("Columns", [400, 240, 220, 40], True, None, False)
row_slider = Button("Row Slider", [55, 220, 30, 80], False, "slider", False)
column_slider = Button("Column Slider", [400, 220, 30, 80], False, "slider", False)

buttons = [
    title_button,
    start_button,
    # bullet_mode,
    # visible_tools,
    # connect4_button,
    # connect5_button,
    # connect6_button,
    # bomb_button,
    # floating_tile_button,
    # magnet_button,
    # freeze_button,
    # set1_button,
    # set2_button,
    # set3_button,
    # low_freq_button,
    # medium_freq_button,
    # high_freq_button,
    rows_label,
    columns_label,
    row_slider,
    column_slider
]

def draw_text(text, big_font, text_col, x, y):
    img = big_font.render(text, True, text_col)
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
            if isinstance(button.appearance, str):
                if button.appearance[-3:] == "png":
                    sprite = pygame.image.load(button.appearance)
                    sprite = pygame.transform.scale(sprite, (60, 60))
                    window.blit(sprite, (button.location[0], button.location[1]))
                
                elif button.is_slider:
                    pygame.draw.rect(window, (120, 52, 25), (button.location[0], button.location[1], 30, 80))
                else:
                    draw_text(button.appearance, big_font, TEXT_COL, button.location[0] + 15, button.location[1])

                if button.status and button.tickable:
                    overlay = pygame.Surface((60, 60), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 100))
                    window.blit(overlay, (button.location[0], button.location[1]))
                    pygame.draw.line(window, (0, 255, 0), (button.location[0] + 0, button.location[1] + 40), (button.location[0] + 20, button.location[1] + 60), 15)
                    pygame.draw.line(window, (0, 255, 0), (button.location[0] + 20, button.location[1] + 60), (button.location[0] + 60, button.location[1] - 10), 15)
                

        draw_text("Board Size", big_font, TEXT_COL, 45, 105)
        draw_text(f"Rows: {config_variables["row_count"]}", small_font, TEXT_COL, 110, 170)
        draw_text(f"Columns: {config_variables["column_count"]}", small_font, TEXT_COL, 430, 170)
        # draw_text("Connect?", big_font, TEXT_COL, 60, 180)
        # draw_text("Powerups", big_font, TEXT_COL, 55, 330)
        # draw_text("Sets to Win", big_font, TEXT_COL, 440, 180)
        # draw_text("Frequency", big_font, TEXT_COL, 445, 330)


        # draw_text(str(config_variables["row_count"]), small_font, TEXT_COL, 150 if config_variables["row_count"] < 10 else 140, 310)
        # draw_text(str(config_variables["column_count"]), small_font, TEXT_COL, 500 if config_variables["column_count"] < 10 else 490, 310)

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

