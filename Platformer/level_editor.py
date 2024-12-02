import pygame

# ========================== SCREEN ===================================
SCREEN_WIDTH = 1248
SCREEN_HEIGHT = 576
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# ======================== FILE PATH ==================================
working_directory = './game_assets/tile_files/'
tile_set_name = 'Tileset.png'
full_file_path = working_directory + tile_set_name
tile_set_image = pygame.image.load(full_file_path).convert()

# ======================= TILE DATA ===================================
tile_set_image_width = tile_set_image.get_width()
tile_set_image_height = tile_set_image.get_height()
tile_width, tile_height = 32, 32
selected_tile = None

def event_checker():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True

def select_tile(mouse_x, mouse_y, selected_tile):
    if mouse_x <= tile_set_image_width and mouse_y <= tile_set_image_height:
        x_tile_index = mouse_x // tile_width
        y_tile_index = mouse_y // tile_height
        if pygame.mouse.get_just_pressed()[0]:
            selected_tile = x_tile_index + tile_set_image_width // tile_width * y_tile_index + 1

            return selected_tile

def draw_tile(selected_tile, screen):
    if selected_tile:
        print(f"Loaded tile {selected_tile}")
        if selected_tile < 10:
            selected_tile = f'0{selected_tile}'
        draw_tile = pygame.image.load(working_directory + f"Tile_{selected_tile}.png").convert()
        screen.blit(draw_tile, (400,400))

running = True
while running:
    running = event_checker()
    screen.blit(tile_set_image, (0, 0))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    selected_tile = select_tile(mouse_x, mouse_y, selected_tile)
    draw_tile(selected_tile, screen)
    pygame.display.update()

pygame.quit()
