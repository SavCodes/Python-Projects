import pygame

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

    def select_tile(self):
        self.mouse_x , self.mouse_y = pygame.mouse.get_pos()
        if self.mouse_x <= self.tile_set_image_width and self.mouse_y <= self.tile_set_image_height:
            x_tile_index = self.mouse_x // self.tile_width
            y_tile_index = self.mouse_y // self.tile_height
            if pygame.mouse.get_just_pressed()[0]:
                self.selected_tile = x_tile_index + self.tile_set_image_width // self.tile_width * y_tile_index + 1

    def draw_tile(self):
        if self.selected_tile:
            print(f"Loaded tile {self.selected_tile}")
            if self.selected_tile < 10:
                self.selected_tile = f'0{self.selected_tile}'

            if pygame.mouse.get_pressed()[0]:
                draw_tile = pygame.image.load(self.working_directory + f"Tile_{self.selected_tile}.png").convert()
                self.screen.blit(draw_tile, (self.mouse_x, self.mouse_y))

    def draw_gridlines(self):
        x_length = (self.screen_width - self.tile_set_image_width) // 32
        y_length = self.screen_height // 32
        for j in range(y_length):
            for i in range(x_length):
                pygame.draw.rect(self.screen, 'white', (self.tile_set_image_width+i*self.tile_width, j*self.tile_height, self.tile_width, self.tile_height),1)


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
        level_editor.select_tile()
        level_editor.draw_tile()
        level_editor.screen.blit(level_editor.tile_set_image)
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()
