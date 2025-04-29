import pygame

class Sounds:
    def __init__(self, is_music, is_powerup, file_name):
        self.is_music = is_music
        self.is_powerup = is_powerup
        self.file_name = f'./assets/sound/{file_name}.wav'
        self.variable_volume = 0.0
        self.sound = None
        self.increasing = False

    def upload_sound(self):
        self.sound = pygame.mixer.Sound(self.file_name)
        self.sound.set_volume(self.variable_volume)
        return self
    
    def start(self, loops = -1, fade_ms = 0):
        self.sound.play(loops = loops, fade_ms = fade_ms)
    
    def set_volume(self, vol):
        self.variable_volume = vol
        if self.sound:
            self.sound.set_volume(vol)
    
    def increase_volume(self, inc):
        self.set_volume(min(self.variable_volume + inc, 1.0))
        return self.variable_volume