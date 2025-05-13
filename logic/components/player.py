class Player:
    def __init__(self, id, player_name, colour, tools):
        self.id = id
        self.player_name = player_name
        self.colour = colour
        self.tools = tools
        self.time = 30
        self.ticks = 0
        self.won = False