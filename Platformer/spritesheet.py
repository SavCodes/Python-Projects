import pygame

class SpriteSheet():
    def __init__(self, sprite_sheet, number_of_animations):
        self.sprites = pygame.image.load(sprite_sheet)
        self.sprite_group = pygame.sprite.Group()
        self.number_of_animations = number_of_animations
        self.frame_list = [self.sprites.subsurface((32*index,0, 32, 32)) for index in range(self.number_of_animations)]















