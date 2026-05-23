import pygame

class SpriteSheet():
    def __init__(self, image, colour):
        self.sheet = image
        self.colour = colour
    
    def get_image(self, frame, width, height, scale, tint = None):
        image = pygame.Surface((width, height)).convert_alpha()
        image.fill(self.colour)
        image.blit(self.sheet, (0, 0), (frame*width, 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(self.colour)

        if tint is not None:
            colouredImage = pygame.Surface(image.get_size())
            colouredImage.fill(tint)
            
            finalImage = image.copy()
            finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
            return finalImage

        return image