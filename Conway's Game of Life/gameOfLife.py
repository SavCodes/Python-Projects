import pygame

class GameBoard:
    def __init__(self, board_size):
        self.board_size = board_size
        # Creates the screen to display the game
        self.screen = pygame.display.set_mode((600, 600))
        self.screen_width, self.screen_height = pygame.display.get_window_size()
        # Creates a 2D array containing cells that track their individual states
        self.cell_states = [[Cell(i,j) for i in range(self.board_size)] for j in range(self.board_size)]
        # Sets the cell width for display based on the board size
        self.set_cell_size()

    def draw_cells(self):
        for row in self.cell_states:
            for cell in row:
                cell.color = "white" if cell.is_alive else "black"
                cell_dimensions = (cell.y_position * cell.width, cell.x_position * cell.width, cell.width, cell.width)
                pygame.draw.rect(self.screen, cell.color, cell_dimensions)

    def set_cell_size(self):
        for row in self.cell_states:
            for cell in row:
                cell.width = self.screen_width / self.board_size

class Cell:
    def __init__(self, x, y):
        self.x_position = x
        self.y_position = y
        self.is_alive = True
        self.color = "black"
        self.width = 1
        self.neighbors = list()

    def __repr__(self):
        return f"Cell({self.x_position}, {self.y_position})"

def event_checker():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True

def initialize_pygame():
    pygame.init()
    pygame.display.set_caption("Game of Life")

def main():
    gameBoard: GameBoard = GameBoard(10)
    gameBoard.set_cell_size()
    gameBoard.draw_cells()
    running = True
    initialize_pygame()
    while running:
        running = event_checker()
        pygame.display.update()
        gameBoard.screen.fill((0, 0, 0))
    pygame.quit()

if __name__ == "__main__":
    main()
