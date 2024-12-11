import pygame

import particle
import pause_menu, button
import level_objective, level_files, level_editor
import player
import physics
import spritesheet
import world_generator
from particle import render_particles
import random

#  MAIN FILE TO DO LIST:
#   -Add darkness around character
#   -Add collision detection for slanted blocks
#   -Add wall slide/jump mechanic for player
#   -Make tracking
#   -Add grass animations

#  LEVEL EDITOR TO DO LIST:
# -Add mechanic to set player spawn
# -Add mechanic to set level objective
# -Add shift click add mechanic


# PLAYER TO DO LIST:
# - Dial in dash mechanic

GAME_SCALE = 2
TILE_SIZE = 32
PANNING_SCREEN_WIDTH = 960
PANNING_SCREEN_HEIGHT = 640
SCREEN_WIDTH = PANNING_SCREEN_WIDTH * 5
SCREEN_HEIGHT = PANNING_SCREEN_HEIGHT * 3
X_WINDOW_PANNING_INDEX = PANNING_SCREEN_WIDTH // (TILE_SIZE * 2 * GAME_SCALE) + 1
Y_WINDOW_PANNING_INDEX = PANNING_SCREEN_HEIGHT // (TILE_SIZE * 4 * GAME_SCALE) + 1
PLAYER_OFFSET_Y = 400
BACKGROUND_SCROLL_FACTOR = 0.1

def initialize_pygame():
    pygame.init()
    pygame.display.set_caption("Platformer Development Testing")

def initialize_player(arrow_controls=True):
    new_player = player.Player(scale=GAME_SCALE, arrow_controls=arrow_controls)
    new_player_screen  = pygame.Surface((PANNING_SCREEN_WIDTH, PANNING_SCREEN_HEIGHT))
    new_player.play_surface = pygame.Surface((SCREEN_WIDTH , SCREEN_HEIGHT)).convert_alpha()
    return new_player, new_player_screen

def load_backgrounds():
    background_directory = "./game_assets/background_images/"
    background_images = []
    for i in range(0,12):
        image = pygame.image.load(f'{background_directory}layer_{i}.png')
        image = pygame.transform.scale(image, (SCREEN_WIDTH ,SCREEN_HEIGHT // 2)).convert_alpha()
        background_images.append(image)
    return background_images

def display_background(player):
    for index, image in enumerate(player.background_list[::-1], 1):
        x_start = calculate_x_start(player.position[0], SCREEN_WIDTH, PANNING_SCREEN_WIDTH)
        display_rect = pygame.Rect(x_start * index * 0.1, player.position[1] + PLAYER_OFFSET_Y - PANNING_SCREEN_HEIGHT // 4, PANNING_SCREEN_WIDTH, PANNING_SCREEN_HEIGHT // 2)
        player.play_surface.blit(image, (x_start, player.position[1] - PANNING_SCREEN_HEIGHT // 4), area=display_rect)

def calculate_x_start(player_position, screen_width, panning_screen_width):
    if player_position <= panning_screen_width // 2:
        return 0
    elif player_position + panning_screen_width > screen_width:
        return screen_width - panning_screen_width
    else:
        return player_position - panning_screen_width // 2

def display_tile_set(player, tile_set):
    x_min = max(min(player.x_ind - X_WINDOW_PANNING_INDEX, 2 * X_WINDOW_PANNING_INDEX), 0)
    x_max = min(player.x_ind + X_WINDOW_PANNING_INDEX + 1, len(tile_set[0]))
    y_min = max(player.y_ind - Y_WINDOW_PANNING_INDEX, 0)
    y_max = min(player.y_ind + Y_WINDOW_PANNING_INDEX + 1, len(tile_set))
    for row in tile_set[y_min:y_max]:
        for tile in row[x_min:x_max]:
            if tile.tile_number != "00":  # Non-empty tile
                tile.draw_platform(player.play_surface)

def event_checker(player_one, player_two, pause_menu):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
        player_one.player_event_checker(event)
        player_two.player_event_checker(event)
        pause_menu.event_checker(event)
    return True

def pan_window(player, player_screen):
    x_start = calculate_x_start(player.position[0], SCREEN_WIDTH, PANNING_SCREEN_WIDTH)
    display_rect = pygame.Rect(x_start, player.position[1] - PANNING_SCREEN_HEIGHT // 4, PANNING_SCREEN_WIDTH, PANNING_SCREEN_HEIGHT // 2)
    player_screen.blit(player.play_surface, area=display_rect)

def run_level_editor(level_editor_button):
    level_editor_button.display_button()
    level_editor_button.check_pressed(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    if level_editor_button.is_pressed:
        level_editor.main(PANNING_SCREEN_WIDTH, PANNING_SCREEN_HEIGHT)

def main():
    running = True
    screen = pygame.display.set_mode((PANNING_SCREEN_WIDTH, PANNING_SCREEN_HEIGHT))
    screen.set_alpha(None)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("comicsans", 30)

    # ===================================== ANIMATED TILE MANAGEMENT ================================================
    # Initialize the AnimatedTileManager
    grass_sway_sheet = spritesheet.SpriteSheet("./game_assets/animated_tiles/grass_spritesheet_41.png", scale=2.0, width=32, height=64)
    tile_manager = spritesheet.AnimatedTileManager()
    for i in range(10):
        tile_manager.add_tile(grass_sway_sheet, (150 + random.randint(30,40)*i,random.randint(350,365)))  # Add at position (200, 150)

    #======================================= PLAYER INITIALIZATION ================================================
    player_one, player_one_screen = initialize_player(arrow_controls=False)
    player_two, player_two_screen = initialize_player(arrow_controls=True)
    player_two.current_level = 0
    player_two.x_spawn, player_two.y_spawn = pygame.math.Vector2(level_files.player_two_spawnpoints[player_two.current_level])  * GAME_SCALE * TILE_SIZE
    player_two.position[0] = player_two.x_spawn
    player_two.direction = -1

    #=======================================PLAYER ONE BACKGROUNDS ================================================
    background_list = load_backgrounds()
    player_one.background_list = background_list
    player_two.background_list = background_list

    # ============================ TILE SET GENERATION ===========================
    player_one.tile_background, player_one.tile_set, player_one.tile_foreground = world_generator.generate_all_world_layers(level_files.player_one_level_set, scale=GAME_SCALE)
    player_two.tile_background, player_two.tile_set, player_two.tile_foreground = world_generator.generate_all_world_layers(level_files.player_two_level_set, scale=GAME_SCALE)

    # ============================= CREATE LEVEL OBJECTIVES =============================
    player_one_test_objective = level_objective.LevelObjective(player_one, SCREEN_WIDTH - 200, 100)
    player_two_test_objective = level_objective.LevelObjective(player_two, 300,100)

    # ============================   PAUSE MENU TESTING =================================
    game_pause_menu = pause_menu.PauseMenu(screen)
    level_editor_button = button.Button(screen, screen.width//2, 40, text="Level Editor" )

    drift_particles = particle.create_particles()

    while running:

        # ========================= CHECK FOR GAME INPUT ===============================
        running = event_checker(player_one, player_two, game_pause_menu)
        if not game_pause_menu.is_paused:

            render_particles(player_one.play_surface, drift_particles, player_one)

            # ============================= PLAYER MOVEMENT ================================
            player_one.get_player_movement()
            player_two.get_player_movement()
            player_one.move_player(player_one.tile_set, screen)
            player_two.move_player(player_two.tile_set, screen)

            # ================================ GRAVITY =====================================
            physics.gravity(player_one)
            physics.gravity(player_two)

            # ============================== COLLISIONS ====================================
            player_one.resolve_collision(player_one.tile_set, screen)
            player_two.resolve_collision(player_two.tile_set, screen)

            # ============================= WINDOW PANNING =================================
            pan_window(player_one, player_one_screen)
            pan_window(player_two, player_two_screen)

            # ========================= DISPLAY BACKGROUND ==================================
            display_background(player_one)
            display_background(player_two)

            # ======================= DISPLAY BACKGROUND TILE SET ====================
            display_tile_set(player_one, player_one.tile_background)
            display_tile_set(player_two, player_two.tile_background)

            # ======================= INDIVIDUAL PLAYER DISPLAY ============================
            player_one.display_player(player_one.play_surface)
            player_two.display_player(player_two.play_surface)

            # ========================= DISPLAY PLAYER LEVEL TILE SET =======================
            display_tile_set(player_one, player_one.tile_set)
            display_tile_set(player_two, player_two.tile_set)

            # ========================= DISPLAY FOREGROUND TILE SET =========================
            display_tile_set(player_one, player_one.tile_foreground)
            display_tile_set(player_two, player_two.tile_foreground)

            # ====================== DISPLAY LEVEL OBJECTIVES ===============================
            player_one_test_objective.display_objective(player_one.play_surface)
            player_two_test_objective.display_objective(player_two.play_surface)

            # ======================== COMBINED PLAYER DISPLAY =============================
            tile_manager.draw_tiles(player_one.play_surface)

            screen.blit(player_one_screen)
            screen.blit(player_two_screen, (0, screen.get_height() // 2))

            # ========================= LEVEL OBJECTIVE LOGIC ==============================
            player_one_test_objective.check_objective_collision()
            player_two_test_objective.check_objective_collision()
            level_objective.check_level_complete(player_one, player_two)

            # ============================= FPS CHECK ============================================
            clock.tick(60)
            fps_text = font.render(f"FPS: {clock.get_fps():.0f}", True, (255, 255, 255))
            fps_text_rect = fps_text.get_rect()
            screen.blit(fps_text, fps_text_rect)

        else:
            screen.fill((255,255,255))
            game_pause_menu.run_pause_menu()
            run_level_editor(level_editor_button)

        pygame.display.update()

if __name__ == '__main__':
    initialize_pygame()
    main()


