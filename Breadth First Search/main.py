import pygame
pygame.init()

def event_checker():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True

def main():
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    running = True
    while running:
        running = event_checker()
        pygame.display.update()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()
