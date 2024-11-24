import pygame
import random

class GameBoard:
    def __init__(self, board_size):
        self.board_size = board_size
        # Creates the screen to display the game
        self.screen = pygame.display.set_mode((600, 600))
        # Grabs screen height and screen width from display
        self.screen_width, self.screen_height = pygame.display.get_window_size()
        # Creates a 2D array containing cells that track their individual states
        self.cell_states = [[Cell(i,j) for i in range(self.board_size)] for j in range(self.board_size)]
        self.set_cell_size()

    def draw_cells(self):
        self.screen.fill((0, 0, 0))
        for row in self.cell_states:
            for cell in row:
                cell.color = "white" if cell.is_alive else "black"
                cell_dimensions = (cell.y_position * cell.width, cell.x_position * cell.width, cell.width, cell.width)
                pygame.draw.rect(self.screen, cell.color, cell_dimensions)

    def set_cell_size(self):
        for row in self.cell_states:
             for cell in row:
                cell.width = self.screen_width / self.board_size

    def find_neighbors(self):
        for row in self.cell_states:
            for cell in row:
                # Assigns neighbors for non-edge cases
                if 0 < cell.x_position < len(self.cell_states) - 1 and 0 < cell.y_position < len(self.cell_states) - 1:
                    cell.neighbors = [self.cell_states[cell.y_position][cell.x_position + 1], # Right Cell
                                      self.cell_states[cell.y_position][cell.x_position - 1], # Left Cell
                                      self.cell_states[cell.y_position - 1][cell.x_position], # Top Cell
                                      self.cell_states[cell.y_position + 1][cell.x_position], # Bottom Cell
                                      self.cell_states[cell.y_position + 1][cell.x_position + 1], # Bottom Right Cell
                                      self.cell_states[cell.y_position + 1][cell.x_position - 1], # Bottom Left Cell
                                      self.cell_states[cell.y_position - 1][cell.x_position + 1], # Top Right Cell
                                      self.cell_states[cell.y_position - 1][cell.x_position - 1], # Top Left Cell
                                      ]
                # Assigns neighbors for top left edge cases
                elif cell.x_position == 0 and cell.y_position == 0:
                    cell.neighbors = [self.cell_states[cell.y_position][cell.x_position + 1], # Right Cell
                                      self.cell_states[cell.y_position + 1][cell.x_position], # Bottom Cell
                                      self.cell_states[cell.y_position + 1][cell.x_position + 1], # Bottom Right Cell
                                      ]
                # Assigns neighbors for top right edge cases
                elif cell.x_position == len(self.cell_states) - 1 and cell.y_position == 0:
                    cell.neighbors = [self.cell_states[cell.y_position][cell.x_position - 1], # Left Cell
                                      self.cell_states[cell.y_position + 1][cell.x_position], # Bottom Cell
                                      self.cell_states[cell.y_position + 1][cell.x_position - 1], # Bottom Left Cell
                                      ]
                # Assigns neighbors for bottom left edge cases
                elif cell.x_position == 0 and cell.y_position == len(self.cell_states) - 1:
                    cell.neighbors = [self.cell_states[cell.y_position][cell.x_position + 1], # Right Cell
                                      self.cell_states[cell.y_position - 1][cell.x_position], # Top Cell
                                      self.cell_states[cell.y_position - 1][cell.x_position + 1], # Top Right Cell
                                      ]
                # Assigns neighbors for bottom right edge cases
                elif cell.x_position == len(self.cell_states) - 1 and cell.y_position == len(self.cell_states) - 1:
                    cell.neighbors = [self.cell_states[cell.y_position][cell.x_position - 1], # Left Cell
                                      self.cell_states[cell.y_position - 1][cell.x_position], # Top Cell
                                      self.cell_states[cell.y_position - 1][cell.x_position - 1], # Top Left Cell
                                      ]
                # Assigns neighbors for left wall edge cases
                elif cell.x_position == 0:
                    cell.neighbors = [self.cell_states[cell.y_position - 1][cell.x_position], # Top Cell
                                      self.cell_states[cell.y_position][cell.x_position + 1], # Right Cell
                                      self.cell_states[cell.y_position + 1][cell.x_position], # Bottom Cell
                                      self.cell_states[cell.y_position + 1][cell.x_position + 1], # Bottom Right Cell
                                      self.cell_states[cell.y_position - 1][cell.x_position + 1]] # Top Right Cell
                # Assigns neighbors for right wall edge cases
                elif cell.x_position == len(self.cell_states) - 1:
                    cell.neighbors = [self.cell_states[cell.y_position][cell.x_position - 1], # Left Cell
                                      self.cell_states[cell.y_position - 1][cell.x_position], # Top Cell
                                      self.cell_states[cell.y_position + 1][cell.x_position], # Bottom Cell
                                      self.cell_states[cell.y_position + 1][cell.x_position - 1], # Bottom Left Cell
                                      self.cell_states[cell.y_position - 1][cell.x_position - 1]] # Top Left Cell
                # Assigns neighbors for top wall edge cases
                elif cell.y_position == 0:
                    cell.neighbors = [self.cell_states[cell.y_position][cell.x_position + 1], # Right Cell
                                      self.cell_states[cell.y_position][cell.x_position - 1], # Left Cell
                                      self.cell_states[cell.y_position + 1][cell.x_position], # Bottom Cell
                                      self.cell_states[cell.y_position + 1][cell.x_position + 1], # Bottom Right Cell
                                      self.cell_states[cell.y_position + 1][cell.x_position - 1], # Bottom Left Cell
                                      ]
                # Assigns neighbors for bottom wall edge cases
                elif cell.y_position == len(self.cell_states) - 1:
                    cell.neighbors = [self.cell_states[cell.y_position][cell.x_position + 1], # Right Cell
                                      self.cell_states[cell.y_position][cell.x_position - 1], # Left Cell
                                      self.cell_states[cell.y_position - 1][cell.x_position], # Top Cell
                                      self.cell_states[cell.y_position - 1][cell.x_position + 1], # Top Right Cell
                                      self.cell_states[cell.y_position - 1][cell.x_position - 1], # Top Left Cell
                                      ]

    def update_living_cells(self, current_gen_cell, next_gen_cell):
        # Rule 1: If a cell has less than two neighbors it dies as if by underpopulation
        if current_gen_cell.live_neighbor_count < 2:
            next_gen_cell.is_alive = False
        # Rule 2: Any cell with two or three neighbors lives on to the next generation
        elif 2 <= current_gen_cell.live_neighbor_count <= 3:
            next_gen_cell.is_alive = True
        # Rule 3: Any live cell with more than three live neighbours dies, as if by overpopulation
        elif current_gen_cell.live_neighbor_count > 3:
            next_gen_cell.is_alive = False

    def update_dead_cells(self, current_gen_cell, next_gen_cell):
        # Rule 4: Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction
        if current_gen_cell.live_neighbor_count == 3:
            next_gen_cell.is_alive = True

    def update_cell_states(self):
        # Creates a copy of the current board state to update alive status for each cell
        next_generation = [[Cell(cell.x_position, cell.y_position, cell.is_alive, cell.neighbors) for cell in row] for row in self.cell_states]

        # Accesses each cell in both the next generation and current generation
        for current_gen_row, next_gen_row in zip(self.cell_states, next_generation):
            for current_gen_cell, next_gen_cell in zip(current_gen_row, next_gen_row):

                # Find the total number of living neighbors
                current_gen_cell.live_neighbor_count = sum(1 for neighbor in current_gen_cell.neighbors if neighbor.is_alive)

                # Update cells in next generation based on game rules:
                if current_gen_cell.is_alive:
                    self.update_living_cells(current_gen_cell, next_gen_cell)
                else:
                    self.update_dead_cells(current_gen_cell, next_gen_cell)

        self.cell_states = next_generation
        self.find_neighbors()

    def randomly_spawn(self, spawn_percentage=50):
        for row in self.cell_states:
            for cell in row:
                if random.randint(0, 100) > spawn_percentage:
                    cell.is_alive = True

class Cell:
    def __init__(self, x, y, is_alive=False, neighbors=[]):
        self.x_position = x
        self.y_position = y
        self.is_alive = is_alive
        self.color = "black"
        self.width = 1
        self.neighbors = neighbors
        self.live_neighbor_count = 0

    def __repr__(self):
        return f"Cell({self.x_position}, {self.y_position}, {self.is_alive})"

def event_checker(game_board):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_board.randomly_spawn()
    return True

def initialize_pygame():
    pygame.init()
    pygame.display.set_caption("Game of Life: Press Spacebar to Randomize Board")

def initialize_game_board(game_size):
    game_board: GameBoard = GameBoard(game_size)
    game_board.find_neighbors()
    game_board.draw_cells()
    game_board.update_cell_states()
    return game_board

def main(game_size):
    initialize_pygame()
    game_board = initialize_game_board(game_size)
    clock = pygame.time.Clock()
    running = True
    while running:
        running = event_checker(game_board)
        game_board.draw_cells()
        pygame.display.update()
        game_board.update_cell_states()
        game_board.set_cell_size()
        clock.tick(15)
    pygame.quit()

if __name__ == "__main__":
    main(50)
