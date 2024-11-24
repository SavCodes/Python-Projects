import pygame

class GameBoard:
    def __init__(self, board_size):
        self.board_size = board_size
        self.cell_states = [Cell(i,j) for i in range(self.board_size) for j in range(self.board_size)]
        print(self.cell_states)

class Cell:
    def __init__(self, x, y):
        self.x_position = x
        self.y_position = y
        self.is_alive = False
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
    running = True
    initialize_pygame()
    screen = pygame.display.set_mode((800, 600))
    while running:
        running = event_checker()
        pygame.display.update()
        screen.fill((0, 0, 0))
    pygame.quit()

if __name__ == "__main__":
    main()
