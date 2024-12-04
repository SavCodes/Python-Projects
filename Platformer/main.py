import pygame

import level_objective
import player
import physics
import world_generator
import level_files
import game_text
import test_file

# TO DO LIST:
#   -Create pause menu
#   -Add collision detection for slanted blocks

GAME_SCALE = 2
PANNING_SCREEN_WIDTH = 960
PANNING_SCREEN_HEIGHT = 640
SCREEN_WIDTH = PANNING_SCREEN_WIDTH * 5
SCREEN_HEIGHT = PANNING_SCREEN_HEIGHT * 3
X_WINDOW_PANNING_INDEX = PANNING_SCREEN_WIDTH // (32 * 2 * GAME_SCALE) + 1
Y_WINDOW_PANNING_INDEX = PANNING_SCREEN_HEIGHT // (32 * 4 * GAME_SCALE) + 1

# ======================================= CREATE INSTRUCTION TEXT =====================================================
arrow_key_intructions = game_text.BouncingText(PANNING_SCREEN_WIDTH//2 - 200, PANNING_SCREEN_HEIGHT + (GAME_SCALE * 32 * 7/4), "Use the Left and Right arrow keys to move")
wasd_intructions = game_text.BouncingText(PANNING_SCREEN_WIDTH * 5 - 250, PANNING_SCREEN_HEIGHT + (GAME_SCALE * 32 * 7/4), "Use the A and D to move left and right")
player_one_jump_instructions = game_text.BouncingText(PANNING_SCREEN_WIDTH//2 + 800, PANNING_SCREEN_HEIGHT + (GAME_SCALE * 32 * 7/4), " Use the Up arrow key to jump ")
player_two_jump_instructions = game_text.BouncingText(PANNING_SCREEN_WIDTH * 5 - 1200, PANNING_SCREEN_HEIGHT + (GAME_SCALE * 32 * 7/4), " Use the Up arrow key to jump ")


def initialize_pygame():
    pygame.init()
    pygame.display.set_caption("Platformer Development Testing")

def event_checker(player_one, player_two):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
        player_one.player_event_checker(event)
        player_two.player_event_checker(event)
    return True

def load_backgrounds():
    background_directory = "./game_assets/background_images/"
    background_images = []
    for i in range(0,4):
        image = pygame.image.load(f'{background_directory}layer_{i}.png')
        image = pygame.transform.scale(image, (SCREEN_WIDTH,SCREEN_HEIGHT // 2))
        image.convert()
        background_images.append(image)
    return background_images

def main(game_scale=1):
    running = True
    initialize_pygame()
    screen = pygame.display.set_mode((PANNING_SCREEN_WIDTH, PANNING_SCREEN_HEIGHT))
    screen.set_alpha(None)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("comicsans", 30)

    #====================================== PLAYER ONE INITIALIZATION ==============================================#
    player_one = player.Player(scale=game_scale, arrow_controls=False)
    player_one_screen = pygame.Surface((screen.get_width(), screen.get_height()//2))
    player_one.play_surface = pygame.Surface((SCREEN_WIDTH , SCREEN_HEIGHT))
    player_one.foreground = pygame.Surface((SCREEN_WIDTH , SCREEN_HEIGHT))

    #======================================== PLAYER ONE BACKGROUNDS ================================================
    player_one.background_list = load_backgrounds()

    #====================================== PLAYER TWO INITIALIZATION ==============================================#
    player_two = player.Player(scale=game_scale)
    player_two_screen = pygame.Surface((screen.get_width(), screen.get_height()//2))
    player_two.play_surface = pygame.Surface((SCREEN_WIDTH , SCREEN_HEIGHT))
    player_two.x_position = PANNING_SCREEN_WIDTH * 5 - 500
    player_two.play_surface.convert()
    player_two.background = pygame.Surface((SCREEN_WIDTH , SCREEN_HEIGHT))
    player_two.foreground = pygame.Surface((SCREEN_WIDTH , SCREEN_HEIGHT))

    #=============================== CONVERT IMAGES FOR ENGINE OPTIMIZATION ======================================
    player_one.play_surface.convert()
    player_one.foreground.convert()
    player_two.play_surface.convert()
    player_two.background.convert()
    player_two.foreground.convert()


    # ============================= LEVEL TILE SET GENERATION ===========================
    player_one_level_set = level_files.player_one_level_set
    player_two_level_set = level_files.player_two_level_set
    player_one.tile_set = world_generator.WorldGenerator(player_one_level_set[player_one.current_level], scale=game_scale).world_tiles
    player_two.tile_set = world_generator.WorldGenerator(player_two_level_set[player_one.current_level], scale=game_scale).world_tiles

    # ============================= CREATE LEVEL OBJECTIVES =============================
    player_one_test_objective = level_objective.LevelObjective(player_one, SCREEN_WIDTH - 200, 100)
    player_two_test_objective = level_objective.LevelObjective(player_two, 300,100)

    while running:

        player_one.get_player_movement()
        player_two.get_player_movement()


        # ====================== DISPLAY LEVEL OBJECTIVES ==============================
        player_one_test_objective.display_objective(player_one.play_surface)
        player_one_test_objective.check_objective_collision()
        player_two_test_objective.display_objective(player_two.play_surface)
        player_two_test_objective.check_objective_collision()
        level_objective.check_level_complete(player_one, player_two)

        # ======================== TUTORIAL INSTRUCTIONS ===============================
        # arrow_key_intructions.display_text(player_one.play_surface)
        # wasd_intructions.display_text(player_two.play_surface)
        # player_one_jump_instructions.display_text(player_one.play_surface)
        # player_two_jump_instructions.display_text(player_two.play_surface)

        # ========================= CHECK FOR GAME INPUT ===============================
        running = event_checker(player_one, player_two)

        # ========================= WINDOW PANNING SETUP ===============================
        player_one_display_rect = pygame.Rect(player_one.x_position- PANNING_SCREEN_WIDTH/2, player_one.y_position - PANNING_SCREEN_HEIGHT // 4, PANNING_SCREEN_WIDTH, PANNING_SCREEN_HEIGHT // 2)
        player_two_display_rect = pygame.Rect(player_two.x_position- PANNING_SCREEN_WIDTH/2, player_two.y_position - PANNING_SCREEN_HEIGHT // 4 , PANNING_SCREEN_WIDTH, PANNING_SCREEN_HEIGHT // 2)


        # ============================= WINDOW PANNING =================================
        player_one_screen.blit(player_one.play_surface , area=player_one_display_rect)
        player_two_screen.blit(player_two.play_surface, area=player_two_display_rect)

        # ============================= PLAYER MOVEMENT ================================
        player_one.move_player(player_one.tile_set, screen)
        player_two.move_player(player_two.tile_set, screen)

        # ================================ GRAVITY =====================================
        physics.gravity(player_one)
        physics.gravity(player_two)

        # ============================== COLLISIONS ====================================
        player_one.resolve_collision(player_one.tile_set, screen)
        player_two.resolve_collision(player_two.tile_set, screen)

        # ============================== DISPLAY RESET =================================
        player_one.play_surface.fill((0,0,0))
        player_two.play_surface.fill((0,0,0))

        # ============================= BACKGROUND DISPLAY
        display_rect = pygame.Rect(player_one.x_position- PANNING_SCREEN_WIDTH/2, player_one.y_position + 400 - PANNING_SCREEN_HEIGHT // 4, PANNING_SCREEN_WIDTH, PANNING_SCREEN_HEIGHT // 2)
        for image in player_one.background_list[::-1]:
            player_one.play_surface.blit(image, (player_one.x_position - PANNING_SCREEN_WIDTH // 2, player_one.y_position-PANNING_SCREEN_HEIGHT//4), area=display_rect)


        # ======================= INDIVIDUAL PLAYER DISPLAY ============================
        player_one.display_player(player_one.play_surface)
        player_two.display_player(player_two.play_surface)

        # ====================== DISPLAY PLAYER ONE TILE MAP =================================
        for layer in player_one.tile_set[max(player_one.y_ind-Y_WINDOW_PANNING_INDEX,0) :player_one.y_ind+Y_WINDOW_PANNING_INDEX]:
            for tile in layer[max(player_one.x_ind-X_WINDOW_PANNING_INDEX,0):min(player_one.x_ind+X_WINDOW_PANNING_INDEX, len(layer))]:
                if tile.tile_number != "00":
                    tile.draw_platform(player_one.play_surface)

        # ====================== DISPLAY PLAYER TWO TILE MAP =================================
        for layer in player_two.tile_set[max(player_two.y_ind-Y_WINDOW_PANNING_INDEX,0):player_two.y_ind+Y_WINDOW_PANNING_INDEX]:
            for tile in layer[max(player_two.x_ind-X_WINDOW_PANNING_INDEX,0):player_two.x_ind+X_WINDOW_PANNING_INDEX]:
                if tile.is_collidable:
                    tile.draw_platform(player_two.play_surface)

        # ======================== COMBINED PLAYER DISPLAY =============================
        screen.blit(player_one_screen)
        screen.blit(player_two_screen, (0, screen.get_height() // 2))

        # ============================= FPS CHECK ============================================
        clock.tick(120)
        fps_text = font.render(f"FPS: {clock.get_fps():.0f}", True, (255, 255, 255))
        fps_text_rect = fps_text.get_rect()
        screen.blit(fps_text, fps_text_rect)
        pygame.display.update()


if __name__ == '__main__':
    main(GAME_SCALE)
