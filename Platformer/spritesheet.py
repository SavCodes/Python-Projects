import pygame

class SpriteSheet():
    def __init__(self, sprite_sheet, scale=1.0):
        self.sprites = pygame.image.load(sprite_sheet)
        self.number_of_animations = int(sprite_sheet.split(".")[0][-1])
        self.sprite_group = pygame.sprite.Group()
        self.scale = scale
        self.frame_list = [self.sprites.subsurface((32*index,0, 32, 32)) for index in range(self.number_of_animations)]
        self.frame_list = [pygame.transform.scale_by(frame, scale) for frame in self.frame_list]














