import pygame

class Ball:
    def __init__(self, screen):
        # Display related attributes
        self.screen = screen
        self.game_width = screen.get_width()
        self.game_height = screen.get_height()

        # Position related attributes
        self.x_position = self.game_width / 2
        self.y_position = self.game_height / 2
        self.radius = 5

        # Movement related attributes
        self.ball_speed = 3
        self.x_velocity = self.ball_speed
        self.y_velocity = self.ball_speed

    def render_ball(self):
        pygame.draw.circle(self.screen, "white", (self.x_position, self.y_position), self.radius)
        self.move_ball()

    def move_ball(self):
        self.x_position += self.x_velocity
        self.y_position += self.y_velocity

    def check_collisions(self, player_one, player_two):
        # Bounces ball off of ceiling and floor
        if not 0 + self.radius < self.y_position < self.game_height - self.radius:
            self.y_velocity *= -1

        # Bounces off left paddle
        elif self.x_position <= player_one.x_position + self.radius + player_one.width and player_one.y_position <= self.y_position <=  player_one.y_position + player_one.height :
            self.x_velocity *= -1

        # Bounces off right paddle
        elif self.x_position >= player_two.x_position and player_two.y_position <= self.y_position <= player_two.y_position + player_two.height :
            self.x_velocity *= -1
