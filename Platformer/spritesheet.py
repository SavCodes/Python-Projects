import pygame

class SpriteSheet():
    def __init__(self, sprite_sheet):
        self.sprites = pygame.image.load(sprite_sheet)
        self.number_of_animations = int(sprite_sheet.split(".")[0][-1])
        self.sprite_group = pygame.sprite.Group()
        self.frame_list = [self.sprites.subsurface((32*index,0, 32, 32)) for index in range(self.number_of_animations)]















