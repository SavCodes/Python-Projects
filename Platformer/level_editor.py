import pygame
import game_tile
import test_file
import world_generator
import level_files
import copy
import button

# TO DO LIST:
# -Add ability to export level data
# -Add camera pan to grid tiles
# -Add a "currently editing `level name`" display

class LevelEditor:
    def __init__(self, font_size=12):
        # ======================== needs to be sorted ============================
        pygame.init()
        self.frame_rate = 300
        self.selected_player = "one"
        self.camera_y_position = 0

        # ======================== CAMERA PANNING ATTRIBUTES ===================
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



        # ========================================= NEEDS SORTING =====================================================
        self.current_level = 0
        #self.level_array = world_generator.WorldGenerator(level_files.player_one_level_set[self.current_level]).world_tiles
        self.level_array = world_generator.WorldGenerator(test_file.player_one_level_0).world_tiles
        self.original_level = copy.deepcopy(self.level_array)
        self.camera_x_position = 0

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
            level_x_index = (self.mouse_x - self.tile_set_image_width) // self.tile_width
            level_y_index = self.mouse_y // self.tile_height
            tile_file = self.working_directory + "Tile_00.png"
            self.level_array[level_y_index][level_x_index] = game_tile.Platform(tile_file, level_x_index*self.tile_width, level_y_index*self.tile_height)

    # ============================= DISPLAY METHODS =========================================
    def display_gridlines(self):
        for j in range(self.level_y_length):
            for i in range(self.level_x_length):
                pygame.draw.rect(self.grid_screen, 'white',
                                 (i * self.tile_width, j * self.tile_height, self.tile_width, self.tile_height), 1)

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
            self.notification_button.display_button()

        # Player two click detection
        self.player_two_button.check_pressed(self.mouse_x, self.mouse_y)
        if self.player_two_button.is_pressed:
            self.selected_player = "two"
            self.notification_button.set_text("Player Two Selected")
            self.notification_button.display_button()

    def check_save_button(self):
        # Check if mouse is hovering button
        self.save_button.check_pressed(self.mouse_x, self.mouse_y)
        if self.save_button.is_pressed:
            with open("test_file.py", "w") as file:
                file.write(f"player_{self.selected_player}_level_{self.current_level} = ")
                file.write(str(self.level_array) + "\n")
            self.notification_button.set_text("Level Saved")
            self.notification_button.display_button()

    def check_reset_button(self):
        self.reset_button.check_pressed(self.mouse_x, self.mouse_y)
        if self.reset_button.is_pressed:
            self.level_array = copy.deepcopy(self.original_level)
            self.notification_button.set_text("Level Reset")
            self.notification_button.display_button()

    def pan_camera(self):
        PANNING_SCREEN_WIDTH = 960
        PANNING_SCREEN_HEIGHT = 576
        panning_display_rect = pygame.Rect(self.camera_x_position,0, PANNING_SCREEN_WIDTH,PANNING_SCREEN_HEIGHT)


        self.screen.blit(self.grid_screen, (self.tile_set_image_width,0), area=panning_display_rect)


def event_checker(level_editor):
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        level_editor.camera_x_position += 15
    elif keys[pygame.K_LEFT]:
        level_editor.camera_x_position -= 15

    for event in events:
        if event.type == pygame.QUIT:
            return False

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
        level_editor.display_tile()
        level_editor.display_gridlines()
        level_editor.screen.blit(level_editor.grid_screen, (level_editor.tile_set_image_width, 0))
        level_editor.pan_camera()
        level_editor.screen.blit(level_editor.tile_set_image)

        # ================================= BUTTON DISPLAY CODE ===================================
        level_editor.player_one_button.display_button()
        level_editor.player_two_button.display_button()
        level_editor.save_button.display_button()
        level_editor.reset_button.display_button()



        # ================================ BUTTON LOGIC CODE =====================================
        level_editor.check_save_button()
        level_editor.check_player_buttons()
        level_editor.check_reset_button()

        # ============================ FPS RELATED LOGIC =============================
        clock.tick(frame_rate)

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
