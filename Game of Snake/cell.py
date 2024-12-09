import pygame

class Cell:
    def __repr__(self):
        return f"Cell {self.x}, {self.y}"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_empty = True
        self.is_food = False

    def update_cell_state(self, snake):
        if [self.x, self.y] in snake.body:
            self.is_empty = False
        else:
            self.is_empty = True

    def draw(self, screen, rows, cols):
        WIDTH = pygame.display.get_window_size()[0] // rows
        rect = (self.x * WIDTH, self.y * WIDTH, WIDTH, WIDTH)
        pygame.draw.rect(screen, "white", pygame.Rect(rect))
