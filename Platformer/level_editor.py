import pygame
import game_tile
import world_generator
import level_files
import copy

# TO DO LIST:
# -Add ability to delete drawn tiles
# -Add ability to export level data
# -Add camera pan to grid tiles
# -Add save and restart buttons

class LevelEditor:
    def __init__(self, font_size=12):
        pygame.init()
        self.frame_rate = 10

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
        self.grid_screen = pygame.Surface((self.screen_width-self.tile_set_image_width, self.screen_height))
        self.level_x_length = (self.screen_width - self.tile_set_image_width) // 32
        self.level_y_length = self.screen_height // 32
        self.level_blank = [[0 for i in range(self.level_x_length)] for j in range(self.level_y_length)]

        # ==================== SAVE BUTTON DATA ===============================
        self.box_width = 100
        self.box_height = 40
        self.save_x_scale = 0.05
        self.save_y_scale = 0.70

        # ==================== RESET BUTTON DATA ===============================
        self.reset_x_scale = 0.15
        self.reset_y_scale = 0.70

        # ==================== PLAYER ONE BUTTON DATA ==============================
        self.player_one_x_scale = 0.05
        self.player_one_y_scale = 0.60

        # ==================== PLAYER TWO BUTTON DATA ==============================
        self.selected_player = "one"
        self.player_two_x_scale = 0.15
        self.player_two_y_scale = 0.60

        self.current_level = 0
        self.level_array = world_generator.WorldGenerator(level_files.player_one_level_set[self.current_level]).world_tiles
        self.original_level = copy.deepcopy(self.level_array)

    def select_tile(self):
        self.mouse_x , self.mouse_y = pygame.mouse.get_pos()
        if self.mouse_x <= self.tile_set_image_width and self.mouse_y <= self.tile_set_image_height:
            x_tile_index = self.mouse_x // self.tile_width
            y_tile_index = self.mouse_y // self.tile_height
            if pygame.mouse.get_just_pressed()[0]:
                self.selected_tile = x_tile_index + self.tile_set_image_width // self.tile_width * y_tile_index + 1

    def draw_tile(self):
        for layer in self.level_array:
            for tile in layer:
                tile.draw_platform(self.grid_screen)

    def add_to_level(self):
        if self.selected_tile and pygame.mouse.get_pressed()[0]:
            level_x_index = (self.mouse_x - self.tile_set_image_width) // self.tile_width
            level_y_index = self.mouse_y // self.tile_height

            if len(str(self.selected_tile)) < 2:
                self.selected_tile = f'0{self.selected_tile}'
            tile_file = f'{self.working_directory}Tile_{self.selected_tile}.png'
            self.level_array[level_y_index][level_x_index] = game_tile.Platform(tile_file, level_x_index*self.tile_width, level_y_index*self.tile_height)

    def draw_gridlines(self):
        for j in range(self.level_y_length):
            for i in range(self.level_x_length):
                pygame.draw.rect(self.grid_screen, 'white', (i*self.tile_width, j*self.tile_height, self.tile_width, self.tile_height),1)

        self.screen.blit(self.grid_screen, (self.tile_set_image_width,0))

    def display_save_box(self):
        save_text = self.font.render("SAVE LEVEL", True, "white")
        save_rect = pygame.Rect(self.screen_width*self.save_x_scale, self.screen_height*self.save_y_scale, self.box_width, self.box_height)
        self.screen.blit(save_text, save_rect)

    def display_reset_box(self):
        reset_text = self.font.render("RESET LEVEL", True, "white")
        reset_rect = pygame.Rect(self.screen_width * self.reset_x_scale, self.screen_height * self.reset_y_scale, self.box_width, self.box_height)
        self.screen.blit(reset_text, reset_rect)

    def display_player_options(self):
        player_one_text = self.font.render("PLAYER ONE", True, "white")
        player_one_rect = pygame.Rect(self.screen_width * self.player_one_x_scale, self.screen_height * self.player_one_y_scale, self.box_width, self.box_height)
        self.screen.blit(player_one_text, player_one_rect)

        player_two_text = self.font.render("PLAYER TWO", True, "white")
        player_two_rect = pygame.Rect(self.screen_width * self.player_two_x_scale, self.screen_height * self.player_two_y_scale, self.box_width, self.box_height)
        self.screen.blit(player_two_text, player_two_rect)

    def click_player_buttons(self):
        # Player one click detection
        if self.screen_width * self.player_one_x_scale < self.mouse_x < self.screen_width * self.player_one_x_scale + self.box_width:
            if self.screen_height * self.player_one_y_scale < self.mouse_y < self.screen_height * self.player_one_y_scale + self.box_height:
                if pygame.mouse.get_pressed()[0]:
                    self.selected_player = "one"

        # Player two click detection
        if self.screen_width * self.player_two_x_scale < self.mouse_x < self.screen_width * self.player_two_x_scale + self.box_width:
            if self.screen_height * self.player_two_y_scale < self.mouse_y < self.screen_height * self.player_two_y_scale + self.box_height:
                if pygame.mouse.get_pressed()[0]:
                    self.selected_player = "two"

    def click_save_button(self):
        new_level_file = copy.deepcopy(self.level_array)
        # Check if mouse is hovering button
        if  self.screen_width * self.save_x_scale < self.mouse_x  < self.screen_width * self.save_x_scale + self.box_width:
            if self.screen_height * self.save_y_scale < self.mouse_y < self.screen_height * self.save_y_scale + self.box_height:
                if pygame.mouse.get_just_pressed()[0]:
                    with open("test_file.py", "a") as file:
                        file.write(f"player_{self.selected_player}_level_{self.current_level} = ")
                        file.write(str(new_level_file) + "\n")
                        print("File saved!")

    def click_reset_button(self):
        if self.screen_width * self.reset_x_scale < self.mouse_x < self.screen_width * self.reset_x_scale + self.box_width:
            if self.screen_height * self.reset_y_scale < self.mouse_y < self.screen_height * self.reset_y_scale + self.box_height:
                if pygame.mouse.get_pressed()[0]:
                    print("clicked reset button")

def event_checker(level_editor):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            level_editor.click_save_button()

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
        level_editor.click_player_buttons()
        level_editor.click_reset_button()
        level_editor.click_save_button()

        # ================================== DISPLAY RELATED CODE ==================================
        level_editor.draw_gridlines()
        level_editor.draw_tile()
        level_editor.screen.blit(level_editor.tile_set_image)
        level_editor.display_player_options()
        level_editor.display_save_box()
        level_editor.display_reset_box()
        pygame.display.update()


        # ============================ FPS RELATED LOGIC =============================
        clock.tick(frame_rate)

    pygame.quit()

if __name__ == '__main__':
    main()
