import pygame

class Paddle:
    def __init__(self, x_position, y_position, controls="arrow_keys"):
        self.controls = controls
        self.x_position = x_position
        self.y_position = y_position
        self.width = 10
        self.height = 60

    def render_paddle(self, screen):
        paddle_dimensions = (self.x_position, self.y_position, self.width, self.height)
        pygame.draw.rect(screen, "white", rect=paddle_dimensions)
