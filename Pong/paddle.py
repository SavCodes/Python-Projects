import pygame

class Paddle:
    def __init__(self, x_position, y_position, arrow_key_controls=True):
        self.move_set = [pygame.K_UP, pygame.K_DOWN] if arrow_key_controls else [pygame.K_w, pygame.K_s]
        self.x_position = x_position
        self.y_position = y_position
        self.width = 10
        self.height = 60
        self.move_speed = 5

    def render_paddle(self, screen):
        self.paddle_event_checker()
        paddle_dimensions = (self.x_position, self.y_position, self.width, self.height)
        pygame.draw.rect(screen, "white", rect=paddle_dimensions)

    def paddle_event_checker(self):
        keys = pygame.key.get_pressed()

        if keys[self.move_set[0]] and self.y_position > 0:
            self.y_position -= self.move_speed
        elif keys[self.move_set[1]] and self.y_position < pygame.display.get_window_size()[1] - self.height:
            self.y_position += self.move_speed

