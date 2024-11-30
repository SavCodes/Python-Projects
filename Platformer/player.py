import pygame
import player
import physics
import game_tile

def initialize_pygame():
    pygame.init()

def event_checker(player_list):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
        for player in player_list:
            player.player_event_checker(event)
    return True

def main():
    running = True

    # Create the players
    player_one = player.Player()
    #player_two = player.Player(arrow_controls=False)

    # Create test tile set for development
    y_tile_set = [game_tile.Platform("Tile_01.png", 0, i*96) for i in range(1,10)] + [game_tile.Platform("Tile_01.png", 960 - 96, i*96) for i in range(1,10)]
    x_tile_set = [game_tile.Platform("Tile_01.png", i*96, 576 - 96) for i in range(1,10,1)]
    tile_set = x_tile_set + y_tile_set

    # Create initial pygame objects
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((960, 576))
    background = pygame.transform.scale(pygame.image.load("Battleground2.png"), (960,576))

    while running:
        running = event_checker([player_one])                       # Check if game was quit
        screen.blit(background)                                     # Refresh the screen between frames

        player_one.move_player(tile_set, screen)                    # Get movement from input and move player
        physics.gravity(player_one)                                 # Apply gravity to player object
        player_one.resolve_collision(tile_set, screen)              # Check for collisions with the world
        player_one.display_player(screen)                           # Draw the player to the screen

        # Other Display
        for tile in tile_set:
            tile.draw_platform(screen)

        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()
