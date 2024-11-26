import pygame

class Player:
    def __init__(self):
        self.screen_width, self.screen_height = 800, 600

        self.player_height = 100
        self.player_width = 20

        self.x_position = self.screen_width / 2
        self.y_position = self.screen_height - self.player_height

    def display_player(self):
        player_rect = (self.x_position, self.y_position, self.player_width, self.player_height)
        player = pygame.draw.rect(pygame.display.get_surface(), (255, 255, 255), player_rect)

def initialize_pygame():
    pygame.init()

def event_checker():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True

def main():
    running = True
    player_one = Player()
    screen = pygame.display.set_mode((800, 600))
    while running:
        running = event_checker()
        player_one.display_player()
        pygame.display.update()

if __name__ == '__main__':
    main()
