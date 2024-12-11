# =========================== DECLARATION OF GAME CONSTANTS ===============================
GAME_SCALE = 2
TILE_SIZE = 32
PANNING_SCREEN_WIDTH = 960
PANNING_SCREEN_HEIGHT = 640
X_WINDOW_PANNING_INDEX = PANNING_SCREEN_WIDTH // (TILE_SIZE * 2 * GAME_SCALE) + 1
Y_WINDOW_PANNING_INDEX = PANNING_SCREEN_HEIGHT // (TILE_SIZE * 4 * GAME_SCALE) + 1
SCREEN_WIDTH = PANNING_SCREEN_WIDTH * 5
SCREEN_HEIGHT = PANNING_SCREEN_HEIGHT * 3
PLAYER_OFFSET_Y = 400
BACKGROUND_SCROLL_FACTOR = 0.1