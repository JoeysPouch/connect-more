import pygame

class SpriteSheet():
    def __init__(self, image, colour):
        self.sheet = image
        self.colour = colour
    
    def get_image(self, frame, width, height, scale, colour = None):
        if colour is None:
            colour = self.colour
        image = pygame.Surface((width, height)).convert_alpha()
        image.fill(colour)
        image.blit(self.sheet, (0, 0), (frame*width, 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)

        return image