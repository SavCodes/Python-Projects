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

        # Initialize player logic
        self.is_touching_ground = True
        self.max_jumps = 2
        self.jump_count = 0

    def display_player(self):
        player_rect = (self.x_position, self.y_position, self.player_width, self.player_height)
        player = pygame.draw.rect(pygame.display.get_surface(), (255, 255, 255), player_rect)

    def move_player(self):
        self.x_position += self.x_velocity
        self.y_position += self.y_velocity
        self.x_velocity += self.x_acceleration
        self.y_velocity += self.y_acceleration

    def get_player_movement(self, keys):
        if keys[pygame.K_LEFT]:
            self.x_velocity = -5
        elif keys[pygame.K_RIGHT]:
            self.x_velocity = 5
        else:
            self.x_velocity = 0

    def jump_player(self):
        if self.jump_count < self.max_jumps:
            self.jump_count += 1
            self.y_velocity = -10

    def ground_check(self):
        if self.y_position > self.screen_height - self.player_height:
            self.is_touching_ground = True
            self.jump_count = 0
        else:
            self.is_touching_ground = False

def gravity(sprite):
    if not sprite.is_touching_ground:
        print("FALLING: ", sprite.y_velocity)
        sprite.y_acceleration = 0.5
    else:
        sprite.y_acceleration = 0
        sprite.y_velocity = 0

def initialize_pygame():
    pygame.init()

def event_checker(player):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.jump_player()

        keys = pygame.key.get_pressed()
        player.get_player_movement(keys)


    return True

def main():
    running = True
    player_one = Player()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))
    while running:
        screen.fill((0, 0, 0))
        running = event_checker(player_one)

        #PLAYER LOGIC
        player_one.move_player()
        player_one.ground_check()
        gravity(player_one)
        player_one.display_player()


        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
