import pygame
import game_tile
import test_file
import world_generator
import level_files
import copy
import button

# TO DO LIST:
# -Add mechanic to set player spawn
# -Add mechanic to set level objective
# -Add shift click add mechanic
# -Add buttons to add/remove foreground
# -Add display for currently selected block
# -Add mechanic to rotate currently selected block

def create_button(x_scale, y_scale, text, screen, tile_set_image_width, width=100, height=40):
    x_position = tile_set_image_width * x_scale
    y_position = pygame.display.get_window_size()[1] * y_scale
    return button.Button(screen, x_position, y_position, width, height, text=text)


class LevelEditor:
    def __init__(self):
        # ======================== needs to be sorted ============================
        pygame.init()
        pygame.display.set_caption('Level Editor')
        self.frame_rate = 300
        self.showing_foreground = False
        self.showing_background = False

        # ======================== CAMERA PANNING ATTRIBUTES ===================
        self.camera_y_position = 0
        self.camera_x_position = 0
        self.TOTAL_LEVEL_WIDTH = 960 * 5
        self.TOTAL_LEVEL_HEIGHT = 576 * 3

        # ======================== FILE PATH ==================================
        self.working_directory = './game_assets/tile_files/'                # CHANGE ME FOR DIFFERENT SETS
        self.tile_set_name = 'Tileset.png'                                  # CHANGE ME FOR DIFFERENT SETS
        self.full_file_path = self.working_directory + self.tile_set_name
        self.tile_set_image = pygame.image.load(self.full_file_path)

        # ======================= SCREEN DATA =================================
        self.screen_width = 1248
        self.screen_height = 576
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # ======================= TILE DATA ===================================
        self.tile_set_image_width = self.tile_set_image.get_width()
        self.tile_set_image_height = self.tile_set_image.get_height()
        self.tile_width, self.tile_height = 32, 32
        self.selected_tile = None

        # ====================== LEVEL DATA ===================================
        self.grid_screen = pygame.Surface((self.TOTAL_LEVEL_WIDTH, self.TOTAL_LEVEL_HEIGHT))
        self.level_x_length = (self.TOTAL_LEVEL_WIDTH - self.tile_set_image_width) // 32
        self.level_y_length = self.TOTAL_LEVEL_HEIGHT // 32

        # ==================== CREATE SETTING BUTTONS ===============================
        self.selected_player = "one"
        self.current_level = 0

        # Left sided buttons
        self.spawn_button = create_button(0.25, 0.50, "SET SPAWN", self.screen, self.tile_set_image_width)
        self.player_one_button = create_button(0.25, 0.60, "PLAYER ONE", self.screen, self.tile_set_image_width)
        self.save_button = create_button(0.25, 0.70, "SAVE LEVEL", self.screen, self.tile_set_image_width)
        self.background_button = create_button(0.25, 0.80, "BACKGROUND", self.screen, self.tile_set_image_width)

        # Right sided buttons
        self.objective_button = create_button(0.75, 0.50, "SET OBJECTIVE", self.screen, self.tile_set_image_width)
        self.player_two_button = create_button(0.75, 0.60, "PLAYER TWO", self.screen, self.tile_set_image_width)
        self.reset_button = create_button(0.75, 0.70, "RESET LEVEL", self.screen, self.tile_set_image_width)
        self.foreground_button = create_button(0.75, 0.80, "FOREGROUND", self.screen, self.tile_set_image_width)

        # Centered buttons
        self.notification_button = create_button(0.50, 0.90, "NOTIFICATIONS", self.screen, self.tile_set_image_width)
        self.level_title_button = create_button(0.45, 0.95, f"Editing: Player {self.selected_player} Level {self.current_level}", self.screen, self.tile_set_image_width)

        # ==================== PLAYER SPAWN LOGIC ==================================
        self.player_spawn_set = False
        self.player_spawn_selected = False

        # ========================================= NEEDS SORTING =====================================================
        self.player_tile_array = world_generator.WorldGenerator(test_file.player_one_level_set[0][self.current_level]).world_tiles
        self.foreground_array = world_generator.WorldGenerator(test_file.player_one_level_set[1][self.current_level]).world_tiles
        self.background_array = world_generator.WorldGenerator(test_file.player_one_level_set[2][self.current_level]).world_tiles

        self.level_array = self.player_tile_array
        self.level_blank = [["00" for i in range(self.level_x_length)] for j in range(self.level_y_length)]
        self.blank_array = world_generator.WorldGenerator(self.level_blank).world_tiles

        self.level_array += self.blank_array[(len(self.level_array) - 1):]
        self.original_level = copy.deepcopy(self.level_array)

    # ========================== EDITING LOGIC METHODS ======================================
    def select_tile(self):
        self.mouse_x , self.mouse_y = pygame.mouse.get_pos()
        if self.mouse_x <= self.tile_set_image_width and self.mouse_y <= self.tile_set_image_height:
            x_tile_index = self.mouse_x // self.tile_width
            y_tile_index = self.mouse_y // self.tile_height
            if pygame.mouse.get_just_pressed()[0]:
                self.selected_tile = x_tile_index + self.tile_set_image_width // self.tile_width * y_tile_index + 1

    def add_to_level(self):
        if self.selected_tile and pygame.mouse.get_pressed()[0] and self.mouse_x > self.tile_set_image_width:
            level_x_index = (self.mouse_x + self.camera_x_position - self.tile_set_image_width) // self.tile_width
            level_y_index = self.mouse_y // self.tile_height

            if len(str(self.selected_tile)) < 2:
                self.selected_tile = f'0{self.selected_tile}'
            tile_file = f'{self.working_directory}Tile_{self.selected_tile}.png'
            self.level_array[level_y_index][level_x_index] = game_tile.Platform(tile_file, level_x_index*self.tile_width, level_y_index*self.tile_height)

        elif pygame.mouse.get_pressed()[2] and self.mouse_x > self.tile_set_image_width:
            level_x_index = (self.mouse_x + self.camera_x_position - self.tile_set_image_width) // self.tile_width
            level_y_index = self.mouse_y // self.tile_height
            tile_file = self.working_directory + "Tile_00.png"
            self.level_array[level_y_index][level_x_index] = game_tile.Platform(tile_file, level_x_index*self.tile_width, level_y_index*self.tile_height)

    def set_player_spawn(self):
        pass

    # ============================= DISPLAY METHODS =========================================
    def display_gridlines(self):
        for j in range(self.level_y_length):
            for i in range(self.level_x_length):
                if (i + j) % 2 == 0:
                    color = (255,255,255)
                else:
                    color = (50,50,50)

                pygame.draw.rect(self.grid_screen, color,
                                 (i * self.tile_width, j * self.tile_height, self.tile_width, self.tile_height))

    def display_tile(self, array_to_display):
        for layer in array_to_display:
            for tile in layer:
                tile.draw_platform(self.grid_screen)

    # ============================ BUTTON METHODS ===========================================
    def check_player_buttons(self):
        # Player one click detection
        self.player_one_button.check_pressed(self.mouse_x, self.mouse_y)
        if self.player_one_button.is_pressed:
            self.selected_player = "one"
            self.notification_button.set_text("Player One Selected")
            self.level_title_button.display_button()
            self.notification_button.display_button((0,0,0))
            self.level_title_button.set_text(f"Editing: Player {self.selected_player} Level {self.current_level}")


        # Player two click detection
        self.player_two_button.check_pressed(self.mouse_x, self.mouse_y)
        if self.player_two_button.is_pressed:
            self.selected_player = "two"
            self.notification_button.set_text("Player Two Selected")
            self.notification_button.display_button((0,0,0))
            self.level_title_button.set_text(f"Editing: Player {self.selected_player} Level {self.current_level}")

    def check_save_button(self):
        # Check if mouse is hovering button
        self.save_button.check_pressed(self.mouse_x, self.mouse_y)
        if self.save_button.is_pressed:
            with open("test_file.py", "a") as file:
                file.write(f"player_{self.selected_player}_level_{self.current_level} = ")
                file.write(str(self.level_array) + "\n")
            self.notification_button.set_text("Level Saved")
            self.notification_button.display_button((0,0,0))

    def check_reset_button(self):
        self.reset_button.check_pressed(self.mouse_x, self.mouse_y)
        if self.reset_button.is_pressed:
            self.level_array = copy.deepcopy(self.original_level)
            self.notification_button.set_text("Level Reset")
            self.notification_button.display_button((0,0,0))

    def check_spawn_button(self):
        self.spawn_button.check_pressed(self.mouse_x, self.mouse_y)
        if self.spawn_button.is_pressed:
            self.player_spawn_selected = True

    def check_foreground_button(self):
        self.foreground_button.check_pressed(self.mouse_x, self.mouse_y)
        if self.foreground_button.is_pressed:
            self.showing_foreground =  not self.showing_foreground

    def check_background_button(self):
        self.background_button.check_pressed(self.mouse_x, self.mouse_y)
        if self.background_button.is_pressed:
            self.showing_background = not self.showing_background

    def pan_camera(self):
        PANNING_SCREEN_WIDTH = 960
        PANNING_SCREEN_HEIGHT = 576
        panning_display_rect = pygame.Rect(self.camera_x_position,0, PANNING_SCREEN_WIDTH,PANNING_SCREEN_HEIGHT)


        self.screen.blit(self.grid_screen, (self.tile_set_image_width,0), area=panning_display_rect)

def event_checker(level_editor):
    # =================== HOLDING KEY LOGIC ========================
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and level_editor.camera_x_position < level_editor.TOTAL_LEVEL_WIDTH:
        level_editor.camera_x_position += 16
    elif keys[pygame.K_LEFT] and level_editor.camera_x_position > 0:
        level_editor.camera_x_position -= 16

    # =================== PRESSING KEY LOGIC =======================
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP and level_editor.current_level < len(test_file.player_one_level_set[level_editor.mask_toggle]) - 1:
            level_editor.current_level += 1
            level_editor.level_array = world_generator.WorldGenerator(test_file.player_one_level_set[level_editor.mask_toggle][level_editor.current_level]).world_tiles
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and level_editor.current_level > 0:
            level_editor.current_level -= 1
            level_editor.level_array = world_generator.WorldGenerator(test_file.player_one_level_set[level_editor.mask_toggle][level_editor.current_level]).world_tiles
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            level_editor.showing_foreground = not level_editor.showing_foreground
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            level_editor.showing_background = not level_editor.showing_background

    return True

def main():
    level_editor = LevelEditor()
    clock = pygame.Clock()
    frame_rate = 300
    running = True
    while running:
        # ================================== LOGIC RELATED CODE ====================================
        running = event_checker(level_editor)
        level_editor.add_to_level()
        level_editor.select_tile()

        # ================================== DISPLAY RELATED CODE ==================================
        level_editor.grid_screen.fill((0,0,0))
        level_editor.screen.fill((0, 0, 0))
        level_editor.display_gridlines()
        level_editor.display_tile(level_editor.player_tile_array)
        level_editor.screen.blit(level_editor.grid_screen, (level_editor.tile_set_image_width, 0))
        if level_editor.showing_background:
            level_editor.display_tile(level_editor.background_array)
        if level_editor.showing_foreground:
            level_editor.display_tile(level_editor.foreground_array)
        level_editor.pan_camera()
        level_editor.screen.blit(level_editor.tile_set_image)

        # ================================= BUTTON DISPLAY CODE ===================================
        level_editor.player_one_button.display_button()
        level_editor.player_two_button.display_button()
        level_editor.save_button.display_button()
        level_editor.reset_button.display_button()
        level_editor.spawn_button.display_button()
        level_editor.objective_button.display_button()
        level_editor.foreground_button.display_button()
        level_editor.background_button.display_button()
        level_editor.level_title_button.display_button((0,0,0))

        # ================================ BUTTON LOGIC CODE =====================================
        level_editor.check_save_button()
        level_editor.check_player_buttons()
        level_editor.check_reset_button()
        level_editor.check_spawn_button()
        level_editor.check_foreground_button()
        level_editor.check_background_button()

        # ============================ FPS RELATED LOGIC =============================
        fps_text = level_editor.save_button.font.render(f"FPS: {clock.get_fps():.0f}", True, (255, 255, 255))
        fps_text_rect = fps_text.get_rect()
        level_editor.screen.blit(fps_text, fps_text_rect)
        clock.tick(frame_rate)
        pygame.display.update()
        clock.tick(90)


    pygame.quit()

if __name__ == '__main__':
    main()
