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


class LevelEditor:
    def __init__(self, font_size=12):
        # ======================== needs to be sorted ============================
        pygame.init()
        self.frame_rate = 300

        # ======================== CAMERA PANNING ATTRIBUTES ===================
        self.camera_y_position = 0
        self.camera_x_position = 0
        self.TOTAL_LEVEL_WIDTH = 960 * 5
        self.TOTAL_LEVEL_HEIGHT = 576 * 3

        # ======================== TEXT ATTRIBUTES =============================
        pygame.display.set_caption('Level Editor')
        self.font_size = font_size
        self.font = pygame.font.SysFont('comicsans', self.font_size)

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
        self.level_blank = [[0 for i in range(self.level_x_length)] for j in range(self.level_y_length)]

        # ==================== SAVE BUTTON DATA ===============================
        self.box_width = 100
        self.box_height = 40
        self.save_x_scale = 0.25
        self.save_y_scale = 0.70
        self.save_x_position = self.tile_set_image_width * self.save_x_scale
        self.save_y_position = self.screen_height * self.save_y_scale
        self.save_button = button.Button(self.screen, self.save_x_position, self.save_y_position,
                                         self.box_width, self.box_height, text="SAVE LEVEL")

        # ==================== RESET BUTTON DATA ===============================
        self.reset_x_scale = 0.75
        self.reset_y_scale = 0.70
        self.reset_x_position = self.tile_set_image_width * self.reset_x_scale
        self.reset_y_position = self.screen_height * self.reset_y_scale
        self.reset_button = button.Button(self.screen, self.reset_x_position, self.reset_y_position,
                                          self.box_width, self.box_height, text="RESET LEVEL")

        # ==================== PLAYER ONE BUTTON DATA ==============================
        self.selected_player = "one"
        self.player_one_x_scale = 0.25
        self.player_one_y_scale = 0.60
        self.player_one_x_position = self.tile_set_image_width * self.player_one_x_scale
        self.player_one_y_position = self.screen_height * self.player_one_y_scale
        self.player_one_button = button.Button(self.screen, self.player_one_x_position, self.player_one_y_position,
                                               self.box_width, self.box_height, text="PLAYER ONE")

        # ==================== PLAYER TWO BUTTON DATA ==============================
        self.player_two_x_scale = 0.75
        self.player_two_y_scale = 0.60
        self.player_two_x_position = self.tile_set_image_width * self.player_two_x_scale
        self.player_two_y_position = self.screen_height * self.player_two_y_scale
        self.player_two_button = button.Button(self.screen, self.player_two_x_position, self.player_two_y_position,
                                               self.box_width, self.box_height, text="PLAYER TWO")

        # =================== NOTIFICATION BUTTON DATA ==============================
        self.notification_x_position = self.tile_set_image_width * 0.50
        self.notification_y_position = self.screen_height * 0.80
        self.notification_button = button.Button(self.screen, self.notification_x_position, self.notification_y_position,
                                                 self.box_width, self.box_height, text="NOTIFICATION")

        # =================== CURRENT LEVEL BUTTON DATA =============================
        self.level_title_x_scale = 0.50
        self.level_title_y_scale = 0.90
        self.current_level = 0
        self.level_title_x_position = self.tile_set_image_width * self.save_x_scale
        self.level_title_y_position = self.screen_height * self.level_title_y_scale
        self.level_title_button = button.Button(self.screen, self.level_title_x_position, self.level_title_y_position,
                                         self.box_width, self.box_height, font_size=20,
                                         text=f"Editing: Player {self.selected_player} Level {self.current_level}")

        # ====================== SPAWN BUTTON DATA ====================================
        self.spawn_button_x_scale = 0.25
        self.spawn_button_y_scale = 0.50
        self.spawn_button_x_position = self.tile_set_image_width * self.spawn_button_x_scale
        self.spawn_button_y_position = self.screen_height * self.spawn_button_y_scale
        self.spawn_button = button.Button(self.screen, self.spawn_button_x_position, self.spawn_button_y_position,
                                          self.box_width, self.box_height, font_size=15, text=f"SET SPAWN")

        # ==================== OBJECTIVE BUTTON DATA ===================================
        self.objective_button_x_scale = 0.75
        self.objective_button_y_scale = 0.50
        self.objective_button_x_position = self.tile_set_image_width * self.objective_button_x_scale
        self.objective_button_y_position = self.screen_height * self.objective_button_y_scale
        self.objective_button = button.Button(self.screen, self.objective_button_x_position, self.objective_button_y_position,
                                          self.box_width, self.box_height, font_size=15, text=f"SET OBJECTIVE")

        # ==================== PLAYER SPAWN LOGIC ==================================
        self.player_spawn_set = False
        self.player_spawn_selected = False

        # ========================================= NEEDS SORTING =====================================================
        #self.level_array = world_generator.WorldGenerator(level_files.player_one_level_set[self.current_level]).world_tiles
        self.level_array = world_generator.WorldGenerator(test_file.player_one_level_set[self.current_level]).world_tiles
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

    def display_tile(self):
        for layer in self.level_array:
            for tile in layer:
                tile.draw_platform(self.grid_screen)

    # ============================ BUTTON METHODS ===========================================
    def check_player_buttons(self):
        # Player one click detection
        self.player_one_button.check_pressed(self.mouse_x, self.mouse_y)
        if self.player_one_button.is_pressed:
            self.selected_player = "one"
            self.notification_button.set_text("Player One Selected")
            self.notification_button.display_button((0,0,0))

        # Player two click detection
        self.player_two_button.check_pressed(self.mouse_x, self.mouse_y)
        if self.player_two_button.is_pressed:
            self.selected_player = "two"
            self.notification_button.set_text("Player Two Selected")
            self.notification_button.display_button((0,0,0))

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
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP and level_editor.current_level < len(test_file.player_one_level_set) - 1:
            level_editor.current_level += 1
            level_editor.level_array = world_generator.WorldGenerator(test_file.player_one_level_set[level_editor.current_level]).world_tiles
            level_editor.level_title_button.set_text(f"Editing: Player {level_editor.selected_player} Level {level_editor.current_level}")
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and level_editor.current_level > 0:
            level_editor.current_level -= 1
            level_editor.level_title_button.set_text(f"Editing: Player {level_editor.selected_player} Level {level_editor.current_level}")
            level_editor.level_array = world_generator.WorldGenerator(test_file.player_one_level_set[level_editor.current_level]).world_tiles

    return True

def main():
    level_editor = LevelEditor()
    clock = pygame.Clock()
    frame_rate = 10
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
        level_editor.display_tile()
        level_editor.screen.blit(level_editor.grid_screen, (level_editor.tile_set_image_width, 0))
        level_editor.pan_camera()
        level_editor.screen.blit(level_editor.tile_set_image)

        # ================================= BUTTON DISPLAY CODE ===================================
        level_editor.player_one_button.display_button()
        level_editor.player_two_button.display_button()
        level_editor.save_button.display_button()
        level_editor.reset_button.display_button()
        level_editor.spawn_button.display_button()
        level_editor.objective_button.display_button()
        level_editor.level_title_button.display_button((0,0,0))

        # ================================ BUTTON LOGIC CODE =====================================
        level_editor.check_save_button()
        level_editor.check_player_buttons()
        level_editor.check_reset_button()
        level_editor.check_spawn_button()

        # ============================ FPS RELATED LOGIC =============================
        clock.tick(frame_rate)
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
