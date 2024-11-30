import pygame
import player
import physics
import world_generator
import level_files

GAME_SCALE = 3

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

def main(game_scale=1):
    running = True

    # Create the players
    player_one = player.Player(scale=game_scale)

    # Create test tile set for development
    tile_set = world_generator.WorldGenerator(level_files.level_one, scale=game_scale).world_tiles

    # Create initial pygame objects
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((960, 576))
    background = pygame.transform.scale(pygame.image.load("Battleground2.png"), (960,576))

    while running:
        running = event_checker([player_one])                       # Check if game was quit
        screen.blit(background)                                     # Refresh the screen between frames

        player_one.move_player(tile_set)                            # Get movement from input and move player
        physics.gravity(player_one)                                 # Apply gravity to player object
        player_one.resolve_collision(tile_set)                      # Check for collisions with the world
        player_one.display_player(screen)                           # Draw the player to the screen

        # Other Display
        for layer in tile_set:
            for tile in layer:
                tile.draw_platform(screen)

        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main(GAME_SCALE)
