import pygame

class Platform:
    def __init__(self,tile, x_position, y_position, is_collidable=True, scale=3):
        self.image = pygame.transform.scale_by(pygame.image.load(tile), scale)
        self.platform_rect = (x_position, y_position, 32, 32)
        self.x_position = x_position
        self.y_position = y_position
        self.is_collidable = is_collidable
        self.collision = None

    def draw_platform(self, screen):
        screen.blit(self.image, self.platform_rect)


