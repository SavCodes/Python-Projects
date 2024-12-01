import pygame
import player
import physics
import world_generator
import level_files

# TO DO LIST:
#   -Optimize collision detection to only check against adjacent tiles
#   -Add camera pan ability
#   -Add level progression mechanic
#   -Create level editor
#   -Create pause menu

GAME_SCALE = 2
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 576

def initialize_pygame():
    pygame.init()
    pygame.display.set_caption("Platformer Development Testing")

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
    initialize_pygame()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create background image for player one
    player_one_background = pygame.transform.scale(pygame.image.load("Battleground2.png"), (SCREEN_WIDTH*5,SCREEN_HEIGHT*5))
    player_one_refresh_background = pygame.transform.scale(pygame.image.load("Battleground2.png"), (SCREEN_WIDTH * 5, SCREEN_HEIGHT * 5))

    # Create background image for player two
    player_two_background = pygame.transform.scale(pygame.image.load("Battleground2.png"), (SCREEN_WIDTH*5,SCREEN_HEIGHT*5))
    player_two_refresh_background = pygame.transform.scale(pygame.image.load("Battleground2.png"), (SCREEN_WIDTH * 5, SCREEN_HEIGHT * 5))


    # Create the players
    player_one = player.Player(scale=game_scale)
    player_two = player.Player(scale=game_scale, arrow_controls=False)
    player_two.x_position = screen.get_width()/2
    player_two.y_position = screen.get_height() - 150

    # Create test tile set for development
    tile_set = world_generator.WorldGenerator(level_files.level_two, scale=game_scale).world_tiles

    # Create initial pygame objects
    clock = pygame.time.Clock()

    while running:

        display_rect = pygame.Rect(player_one.x_position- SCREEN_WIDTH/2, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        running = event_checker([player_one, player_two])           # Check if game was quit
        screen.blit(player_one_background , area=display_rect)                 # Draw updated scene to screen
        player_one_background.blit(player_one_refresh_background)                         # Refresh the screen between frames

        player_one.move_player(tile_set, screen)                    # Get movement from input and move player
        physics.gravity(player_one)                                 # Apply gravity to player object
        player_one.resolve_collision(tile_set, screen)              # Check for collisions with the world
        player_one.display_player(player_one_background)                       # Draw the player to the screen

        player_two.move_player(tile_set, screen)                    # Get movement from input and move player
        physics.gravity(player_two)                                 # Apply gravity to player object
        player_two.resolve_collision(tile_set, screen)              # Check for collisions with the world
        player_two.display_player(player_one_background)                       # Draw the player to the screen

        # Other Display
        for layer in tile_set:
            for tile in layer:
                tile.draw_platform(player_one_background)

        pygame.display.update()
        clock.tick()

if __name__ == '__main__':
    main(GAME_SCALE)
