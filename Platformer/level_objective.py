import pygame
import world_generator
import level_files

from main import GAME_SCALE

class LevelObjective:
    def __init__(self, player, x_position, y_position, game_scale=1):
        self.player = player
        self.game_scale = game_scale
        self.x_position = x_position
        self.y_position = y_position
        self.color = (255,0,0)
        self.width = 32 * self.game_scale
        self.height = 32 *  GAME_SCALE * 2

    def display_objective(self, screen):
        self.objective_rect = pygame.Rect(self.x_position, self.y_position, self.width, self.height)
        pygame.draw.rect(screen, self.color, self.objective_rect, 3)

    def check_objective_collision(self, player):
        if player.player_rect.colliderect(self.objective_rect):
            player.current_level += 1
            player.tile_set = world_generator.WorldGenerator(level_files.player_one_level_set[player.current_level], scale=GAME_SCALE).world_tiles
            player.x_position = 300


