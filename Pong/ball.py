import pygame

class Ball:
    def __init__(self, screen):
        # Display related attributes
        self.screen = screen
        self.game_width = screen.get_width()
        self.game_height = screen.get_height()

        # Position related attributes
        self.x_position = 400
        self.y_position = 400
        self.radius = 5

        # Movement related attributes
        self.ball_speed = 3
        self.x_velocity = 0
        self.y_velocity = self.ball_speed

    def render_ball(self):
        pygame.draw.circle(self.screen, "white", (self.x_position, self.y_position), self.radius)
        self.move_ball()
        self.check_boundaries()

    def check_boundaries(self):
        if not 0 + self.radius < self.y_position < self.game_height - self.radius:
            self.y_velocity *= -1

    def move_ball(self):
        self.x_position += self.x_velocity
        self.y_position += self.y_velocity
