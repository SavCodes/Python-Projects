import pygame
import paddle

def event_checker():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

pygame.init()

def main():
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    player_one = paddle.Paddle(400, 300)
    running = True
    while running:
        screen.fill((0, 0, 0))
        running = event_checker()
        player_one.render_paddle(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
