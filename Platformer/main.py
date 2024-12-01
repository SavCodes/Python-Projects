import pygame
import player
import physics
import world_generator
import level_files

# TO DO LIST:
#   -Clamp window panning to level boundaries
#   -Draw only on screen tiles
#   -Add level progression mechanic
#   -Create level editor
#   -Create pause menu

GAME_SCALE = 2
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 576
X_WINDOW_PANNING_INDEX = SCREEN_WIDTH // (32 * 2 * GAME_SCALE) + 1
Y_WINDOW_PANNING_INDEX = SCREEN_HEIGHT // (32 * 4 * GAME_SCALE) + 1

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
    font = pygame.font.SysFont("comicsans", 30)

    #====================================== PLAYER ONE INITIALIZATION ==============================================#
    player_one = player.Player(scale=game_scale)
    player_one_screen = pygame.Surface((screen.get_width(), screen.get_height()//2))
    player_one_background = pygame.Surface((SCREEN_WIDTH * 5 , SCREEN_HEIGHT * 3))
    player_one_refresh_background = pygame.Surface((SCREEN_WIDTH * 5, SCREEN_HEIGHT * 2))
    player_one_background.convert()
    player_one_refresh_background.convert()

    #====================================== PLAYER TWO INITIALIZATION ==============================================#
    player_two = player.Player(scale=game_scale, arrow_controls=False)
    player_two_screen = pygame.Surface((screen.get_width(), screen.get_height()//2))
    player_two_background = pygame.Surface((SCREEN_WIDTH * 5 , SCREEN_HEIGHT * 3))
    player_two_refresh_background = pygame.Surface((SCREEN_WIDTH * 5, SCREEN_HEIGHT * 2))
    player_two.x_position = screen.get_width()/2 + 100
    player_two.y_position = screen.get_height() - 150
    player_two_background.convert()
    player_two_refresh_background.convert()

    # ============================= LEVEL TILE SET GENERATION ===========================
    player_one_tile_set = world_generator.WorldGenerator(level_files.player_one_level_two, scale=game_scale).world_tiles
    player_two_tile_set = world_generator.WorldGenerator(level_files.player_two_level_two, scale=game_scale).world_tiles

    while running:
        # Check if game was quit
        running = event_checker([player_one, player_two])
        #player_one_background = player_one_refresh_background

        # ========================= WINDOW PANNING SETUP ===============================
        player_one_display_rect = pygame.Rect(player_one.x_position- SCREEN_WIDTH/2, player_one.y_position - SCREEN_HEIGHT // 4, SCREEN_WIDTH, SCREEN_HEIGHT // 2)
        player_two_display_rect = pygame.Rect(player_two.x_position- SCREEN_WIDTH/2, player_two.y_position - SCREEN_HEIGHT // 4 , SCREEN_WIDTH, SCREEN_HEIGHT // 2)

        # ============================= WINDOW PANNING =================================
        player_one_screen.blit(player_one_background , area=player_one_display_rect)
        player_two_screen.blit(player_two_background, area=player_two_display_rect)

        # ============================== DISPLAY RESET =================================
        player_one_background.blit(player_one_refresh_background)
        player_two_background.blit(player_two_refresh_background)

        # ============================= PLAYER MOVEMENT ================================
        player_one.move_player(player_one_tile_set, screen)
        player_two.move_player(player_two_tile_set, screen)

        # ================================ GRAVITY =====================================
        physics.gravity(player_one)
        physics.gravity(player_two)

        # ============================== COLLISIONS ====================================
        player_one.resolve_collision(player_one_tile_set, screen)
        player_two.resolve_collision(player_two_tile_set, screen)

        # ======================= INDIVIDUAL PLAYER DISPLAY ============================
        player_one.display_player(player_one_background)
        player_two.display_player(player_two_background)

        # ======================== COMBINED PLAYER DISPLAY =============================
        screen.blit(player_one_screen)
        screen.blit(player_two_screen, (0, screen.get_height() // 2))

        # =========================== DISPLAY TILE MAP =================================
        for layer in player_one_tile_set[player_one.y_ind-Y_WINDOW_PANNING_INDEX:player_one.y_ind+Y_WINDOW_PANNING_INDEX]:
            for tile in layer[player_one.x_ind-X_WINDOW_PANNING_INDEX:player_one.x_ind+X_WINDOW_PANNING_INDEX]:
                tile.draw_platform(player_one_background)

        for layer in player_two_tile_set:
            for tile in layer[player_two.x_ind-X_WINDOW_PANNING_INDEX:player_two.x_ind+X_WINDOW_PANNING_INDEX]:
                tile.draw_platform(player_two_background)

        # ============================= FPS CHECK =====================================
        clock.tick(60)
        fps_text = font.render(f"FPS: {clock.get_fps():.0f}", True, (255, 255, 255))
        fps_text_rect = fps_text.get_rect()
        screen.blit(fps_text, fps_text_rect)

        pygame.display.update()


if __name__ == '__main__':
    main(GAME_SCALE)
