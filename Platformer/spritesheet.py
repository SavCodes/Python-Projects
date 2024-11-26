import pygame

class SpriteSheet:
    def __init__(self, sprite_sheet):
        self.sprite = pygame.image.load(sprite_sheet)
        self.frame_list = []

    def get_frames(self, frame, width, height, scale, color):
        image = pygame.Surface((width,height))
        image.blit(self.sprite, (0,0), ((frame*width), 0, width, height))
        image.set_colorkey(color)
        image = pygame.transform.scale(image, (width*scale, height*scale))
        return image











