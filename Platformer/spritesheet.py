import pygame

class SpriteSheet():
    def __init__(self, sprite_sheet):
        self.sprites = pygame.image.load(sprite_sheet)
        self.sprite_group = pygame.sprite.Group()

    def get_frames(self, width, height, scale, color):
        number_of_frames = self.sprites.get_width() // width
        for frame in range(number_of_frames):
            image = pygame.Surface((width,height))
            image.set_colorkey(color)
            image = pygame.transform.scale(image, (width*scale, height*scale))
            image = image.blit(self.sprites, (0,0), ((frame*width), 0, width, height))
            FRAME = Frame(image)
            self.sprite_group.add(FRAME)

class Frame(pygame.sprite.Sprite):
    def __init__(self, frame):
        pygame.sprite.Sprite.__init__(self)












