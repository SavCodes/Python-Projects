# TO DO LIST:
#      - Fix food spawning underneath snake
#      - Add running score visual while playing
#      - Add difficulty slider
#      - Add music, application icon, application name
#      - Add grid pattern to board
#      - Add an endless mode option
#      - Make code dynamic to different window settings, and gamestate matrix sizes


# Import required libraries
import pygame
import random
import sys

# Initialize pygame requirements
pygame.init()
screen = pygame.display.set_mode((600, 600))

# Cell object used to track the state of each traversable space
class Cell:
    def __repr__(self):
        return f"Cell {self.x}, {self.y}"
      
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_empty = True
        self.is_food = False

    def draw(self, screen, rows, cols):
        WIDTH = pygame.display.get_window_size()[0] // rows
        rect = (self.x * WIDTH, self.y * WIDTH, WIDTH, WIDTH)
        pygame.draw.rect(screen, "white", pygame.Rect(rect))
      
    def update_cell_state(self, snake):
        if [self.x, self.y] in snake.body:
            self.is_empty = False
        else:
            self.is_empty = True

class Snake:
    def __init__(self, screen, rows, cols):
        self.screen = screen
        self.rows, self.cols = rows, cols
        self.head_x, self.head_y = cols // 2, rows // 2
        self.body = [[self.head_x, self.head_y]]
        self.length = 1
        self.move = [-1,0]

    def draws(self):
        width = pygame.display.get_window_size()[0] // self.rows
        for segment in self.body:
            rect = (segment[0] * width, segment[1] * width, width, width)
            pygame.draw.rect(self.screen, "red", pygame.Rect(rect))

    def get_move(self, event):
        if event.key == pygame.K_w or event.key == pygame.K_UP:
            self.move = [0, -1]
        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
            self.move = [0, 1]
        elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
            self.move = [-1, 0]
        elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            self.move = [1, 0]

    def moves(self):
        x_move, y_move = self.move
        new_head = [[self.body[0][0] + x_move, self.body[0][1] + y_move]]
        self.body = new_head + self.body[:-1]
        self.head_x, self.head_y = self.body[0]

    def grow(self):
        tail_x, tail_y = self.body[-1]
        new_tail_x = tail_x + (-self.move[0])
        new_tail_y = tail_y + (-self.move[1])
        self.body.append([new_tail_x, new_tail_y])
        self.length += 1

    def check_collisions(self, gamestates):
        exit_message = f"YOU LOSE! Score: {self.length}"
        if self.head_x < 0 or self.head_y < 0:
            sys.exit(exit_message)
        elif self.head_x > self.cols - 1 or self.head_y > self.rows - 1:
            sys.exit(exit_message)
        elif [self.head_x, self.head_y] in self.body[1:]:
            sys.exit(exit_message)

class Food:
    def __init__(self, gamestates, screen):
        self.gamestates = gamestates
        self.screen = screen
        self.x = random.randint(0, len(self.gamestates[0]) - 1)
        self.y = random.randint(0, len(self.gamestates) - 1)
        self.width = screen.get_width() / len(self.gamestates[0])

    def spawn_food(self):
        food_width = 10
        target_position =  self.gamestates[self.y][self.x]
        if target_position.is_empty:
            target_position.is_food = True
        rect_x = target_position.x * self.width + (self.width - food_width) / 2
        rect_y = target_position.y * self.width + (self.width - food_width) / 2
        food_rect = rect_x, rect_y, food_width, food_width
        pygame.draw.rect(self.screen, "green", pygame.Rect(food_rect))

    def eat_food(self, snake):
        curr_position = [snake.head_x, snake.head_y]
        next_position = [snake.head_x + snake.move[0], snake.head_y + snake.move[1]]

        if next_position == [self.x, self.y] or curr_position == [self.x, self.y]:
            self.x = random.randint(0, len(self.gamestates[0]) - 1)
            self.y = random.randint(0, len(self.gamestates) - 1)
            snake.grow()

def initialize_gamestates(rows, cols):
    gamestates = [[Cell(i,j) for i in range(rows)] for j in range(cols)]
    for row in gamestates:
        for cell in row:
            cell.draw(screen, rows, cols)
    return gamestates

def event_checker(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit("Thanks for playing!")
        elif event.type == pygame.KEYDOWN:
            snake.get_move(event)

def main(screen, ROWS, COLS):
    clock = pygame.time.Clock()
    gamestates = initialize_gamestates(ROWS, COLS)
    snake = Snake(screen, ROWS, COLS)
    food = Food(gamestates, screen)
    while True:
        screen.fill("white")
        food.eat_food(snake)
        event_checker(snake)
        snake.moves()
        food.spawn_food()
        snake.draws()
        snake.check_collisions(gamestates)
        pygame.display.flip()
        clock.tick(6)
        for row in gamestates:
            for cell in row:
                cell.update_cell_state(snake)

if __name__ == "__main__":
    main(screen, 10, 10)
