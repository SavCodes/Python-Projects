import pygame
import player
import physics
import world_generator
import level_files

# TO DO LIST:
#   -Change world generation so players each have their own levels
#   -Draw only on screen tiles
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
    clock = pygame.time.Clock()

    #====================================== PLAYER ONE INITIALIZATION ==============================================#
    player_one = player.Player(scale=game_scale)
    player_one_screen = pygame.Surface((screen.get_width(), screen.get_height()//2))
    player_one_background = pygame.transform.scale(pygame.image.load("Battleground2.png"), (SCREEN_WIDTH*5,SCREEN_HEIGHT*5))
    player_one_refresh_background = pygame.transform.scale(pygame.image.load("Battleground2.png"), (SCREEN_WIDTH * 5, SCREEN_HEIGHT * 5))

    #====================================== PLAYER TWO INITIALIZATION ==============================================#
    player_two = player.Player(scale=game_scale, arrow_controls=False)
    player_two_screen = pygame.Surface((screen.get_width(), screen.get_height()//2))
    player_two_background = pygame.transform.scale(pygame.image.load("Battleground3.png"), (SCREEN_WIDTH*5,SCREEN_HEIGHT*5))
    player_two_refresh_background = pygame.transform.scale(pygame.image.load("Battleground3.png"), (SCREEN_WIDTH * 5, SCREEN_HEIGHT * 5))
    player_two.x_position = screen.get_width()/2
    player_two.y_position = screen.get_height() - 150

    # Create test tile set for development
    tile_set = world_generator.WorldGenerator(level_files.level_two, scale=game_scale).world_tiles

    while running:
        # Check if game was quit
        running = event_checker([player_one, player_two])

        # ========================= WINDOW PANNING SETUP ===============================
        player_one_display_rect = pygame.Rect(player_one.x_position- SCREEN_WIDTH/2, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2)
        player_two_display_rect = pygame.Rect(player_two.x_position- SCREEN_WIDTH/2, SCREEN_HEIGHT //2 , SCREEN_WIDTH, SCREEN_HEIGHT // 2)

        # ============================= WINDOW PANNING =================================
        player_one_screen.blit(player_one_background , area=player_one_display_rect)
        player_two_screen.blit(player_two_background, area=player_two_display_rect)

        # ============================== DISPLAY RESET =================================
        player_one_background.blit(player_one_refresh_background)
        player_two_background.blit(player_two_refresh_background)

        # ============================= PLAYER MOVEMENT ================================
        player_one.move_player(tile_set, screen)
        player_two.move_player(tile_set, screen)

        # ================================ GRAVITY =====================================
        physics.gravity(player_one)
        physics.gravity(player_two)

        # ============================== COLLISIONS ====================================
        player_one.resolve_collision(tile_set, screen)
        player_two.resolve_collision(tile_set, screen)

        # ======================= INDIVIDUAL PLAYER DISPLAY ============================
        player_one.display_player(player_one_background)
        player_two.display_player(player_two_background)

        # ======================== COMBINED PLAYER DISPLAY =============================
        screen.blit(player_one_screen)
        screen.blit(player_two_screen, (0, screen.get_height() // 2))

        # =========================== DISPLAY TILE MAP =================================
        for layer in tile_set:
            for tile in layer:
                tile.draw_platform(player_one_background)
                tile.draw_platform(player_two_background)

        pygame.display.update()

        clock.tick()

if __name__ == '__main__':
    main(GAME_SCALE)
