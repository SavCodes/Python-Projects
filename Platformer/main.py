import pygame

class Player:
    def __init__(self):
        self.screen_width, self.screen_height = 800, 600

        # Initialize player dimensions
        self.player_height = 100
        self.player_width = 20

        # Initialize player position
        self.x_position = self.screen_width / 2
        self.y_position = self.screen_height - self.player_height

        # Initialize player velocities
        self.x_velocity = 0
        self.y_velocity = 0

        # Initialize player accelerations
        self.x_acceleration = 0
        self.y_acceleration = 0


    def display_player(self):
        player_rect = (self.x_position, self.y_position, self.player_width, self.player_height)
        player = pygame.draw.rect(pygame.display.get_surface(), (255, 255, 255), player_rect)


    def move_player(self):
        self.x_position += self.x_velocity
        self.y_position += self.y_velocity
        self.x_velocity += self.x_acceleration
        self.y_velocity += self.y_acceleration


def initialize_pygame():
    pygame.init()

def event_checker(player):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
        keys = pygame.key.get_pressed()

            # Move player based on pressed keys
        if keys[pygame.K_LEFT]:
            player.x_velocity = -0.5
        if keys[pygame.K_RIGHT]:
            player.x_velocity = 0.5
        if keys[pygame.K_UP]:
            player.y_velocity = -0.5
        if keys[pygame.K_DOWN]:
            player.y_velocity = 0.5
    return True

def main():
    running = True
    player_one = Player()
    screen = pygame.display.set_mode((800, 600))
    while running:
        screen.fill((0, 0, 0))
        running = event_checker(player_one)

        #PLAYER LOGIC
        player_one.move_player()
        player_one.display_player()

        pygame.display.update()

if __name__ == '__main__':
    main()
