import pygame
import player
import physics

def initialize_pygame():
    pygame.init()

def event_checker(player):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
        player.player_event_checker(event)
    return True

def main():
    running = True
    player_one = player.Player()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))
    background = pygame.transform.scale(pygame.image.load("Battleground2.png"), (800,600))
    while running:
        running = event_checker(player_one)

        # Player Logic
        player_one.move_player()
        player_one.ground_check()
        physics.gravity(player_one)


        # Plyer Display
        screen.blit(background)
        player_one.display_player(screen)
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
