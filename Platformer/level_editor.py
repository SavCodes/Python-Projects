import pygame
import game_tile
import world_generator

class LevelEditor:
    def __init__(self):
        pygame.init()
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
        self.level_array =  world_generator.WorldGenerator(self.level_blank).world_tiles

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

            if int(self.selected_tile) < 10:
                self.selected_tile = f'0{self.selected_tile}'
            tile_file = f'{self.working_directory}Tile_{self.selected_tile}.png'
            self.level_array[level_y_index][level_x_index] = game_tile.Platform(tile_file, level_x_index*self.tile_width, level_y_index*self.tile_height)

    def draw_gridlines(self):
        for j in range(self.level_y_length):
            for i in range(self.level_x_length):
                pygame.draw.rect(self.grid_screen, 'white', (i*self.tile_width, j*self.tile_height, self.tile_width, self.tile_height),1)

        self.screen.blit(self.grid_screen, (self.tile_set_image_width,0))

def event_checker():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True

def main():
    level_editor = LevelEditor()

    running = True
    while running:
        running = event_checker()
        level_editor.draw_gridlines()
        level_editor.add_to_level()
        level_editor.select_tile()

        level_editor.draw_tile()
        level_editor.screen.blit(level_editor.tile_set_image)
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()
