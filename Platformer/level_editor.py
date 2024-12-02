import pygame

SCREEN_WIDTH = 1248
SCREEN_HEIGHT = 576
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
tile_set_image = pygame.image.load('./game_assets/tile_files/Tileset.png')
tile_set_image_width = tile_set_image.get_width()
tile_set_image_height = tile_set_image.get_height()
tile_width, tile_height = 32, 32

def event_checker():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True

def select_tile(mouse_x, mouse_y):
    if mouse_x <= tile_set_image_width and mouse_y <= tile_set_image_height:
        x_tile_index = mouse_x // tile_width
        y_tile_index = mouse_y // tile_height
        return x_tile_index + y_tile_index * tile_set_image_width//32 + 1


running = True
while running:
    running = event_checker()
    screen.blit(tile_set_image, (0, 0))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    selected_tile = select_tile(mouse_x, mouse_y)
    pygame.display.update()

pygame.quit()
