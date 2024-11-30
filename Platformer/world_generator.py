import game_tile

class WorldGenerator:
    def __init__(self, world_array_2d, scale=1):
        self.world_array = world_array_2d
        self.scale = scale
        self.world_tiles = [[game_tile.Platform(f"Tile_0{tile}.png", x_index * 32 * self.scale,
                                                y_index * 32 * self.scale, scale=self.scale, is_collidable=tile) for
                             x_index, tile in enumerate(layer)] for y_index, layer in enumerate(self.world_array)]



