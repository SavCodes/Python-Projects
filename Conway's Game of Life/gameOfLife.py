import pygame

class Cell:
    def __init__(self, x, y):
        self.x_position = x
        self.y_position = y
        self.is_alive = False
           
def event_checker():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True

def initialize_pygame():
    pygame.init()
    pygame.display.set_caption("Game of Life")

def main():
    running = True
    initialize_pygame()
    screen = pygame.display.set_mode((800, 600))
    while running:
        running = event_checker()
        pygame.display.update()
        screen.fill((0, 0, 0))
    pygame.quit()

if __name__ == "__main__":
    main()
