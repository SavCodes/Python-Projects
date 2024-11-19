import pygame
import random
import sys
import time

# TO DO LIST:
#      - Add difficulty slider
#      - Add grid pattern to board
#      - Add an endless mode option

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

class Snake:
    def __init__(self, screen, gamestates):
        self.gamestates = gamestates
        self.screen = screen
        self.rows, self.cols = len(gamestates), len(gamestates[0])
        self.head_x, self.head_y = self.cols // 2, self.rows // 2
        self.body = [[self.head_x, self.head_y]]
        self.length = 0
        self.move = [-1,0]
        self.grow_sound = pygame.mixer.Sound("grow.wav")
        self.lose_sound = pygame.mixer.Sound("game_over.wav")

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
        self.grow_sound.play()
        tail_x, tail_y = self.body[-1]
        new_tail_x = tail_x + (-self.move[0])
        new_tail_y = tail_y + (-self.move[1])
        self.body.append([new_tail_x, new_tail_y])
        self.length += 1

    def check_collisions(self):
        # Checks for collision with walls ----------------------------------------------:
        if not 0 <= self.head_x <= self.cols -1 or not 0 <= self.head_y <= self.rows -1:
            self.lose_sound.play()
            time.sleep(2)
            sys.exit(f"GAME OVER: Crashed into wall! Final Score: {self.length}")

        # Checks for collision with self -----------------------------------------------:
        elif [self.head_x, self.head_y] in self.body[1:]:
            self.lose_sound.play()
            time.sleep(2)
            sys.exit(f"GAME OVER: Crashed into self! Final Score: {self.length}")

    def display_score(self):
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render(f"{self.length}", False, "red")
        self.screen.blit(text_surface, dest=(0, 0))

    def update_gamestates(self):
        for row in self.gamestates:
            for cell in row:
                if [cell.x, cell.y] in self.body:
                    self.gamestates[cell.y][cell.x].is_empty = False
                else:
                    self.gamestates[cell.y][cell.x].is_empty = True

class Food:
    def __init__(self, gamestates, screen):
        self.screen = screen
        self.x = random.randint(0, len(gamestates[0]) - 1)
        self.y = random.randint(0, len(gamestates) - 1)
        self.width = screen.get_width() / len(gamestates[0])

    def spawn_food(self, snake):
        food_width = 10
        target_position =  snake.gamestates[self.y][self.x]
        if target_position.is_empty:
            target_position.is_food = True
            rect_x = target_position.x * self.width + (self.width - food_width) / 2
            rect_y = target_position.y * self.width + (self.width - food_width) / 2
            food_rect = rect_x, rect_y, food_width, food_width
            pygame.draw.rect(self.screen, "green", pygame.Rect(food_rect))
        else:
            self.x = random.randint(0, len(snake.gamestates[0]) - 1)
            self.y = random.randint(0, len(snake.gamestates) - 1)

    def eat_food(self, snake):
        curr_position = [snake.head_x, snake.head_y]
        next_position = [snake.head_x + snake.move[0], snake.head_y + snake.move[1]]
        if next_position == [self.x, self.y] or curr_position == [self.x, self.y]:
            self.x = random.randint(0, len(snake.gamestates[0]) - 1)
            self.y = random.randint(0, len(snake.gamestates) - 1)
            snake.grow()

def initialize_pygame(width, height):
    pygame.init()

    # Visual Initializations -------------------------------------------------------
    screen = pygame.display.set_mode((width, height))
    pygame_icon = pygame.image.load('snake.png')
    pygame.display.set_icon(pygame_icon)
    pygame.display.set_caption("Classic game of snake brought to you by SavCodes!")

    # Audio Initializations --------------------------------------------------------
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.play(-1)

    return screen

def initialize_gamestates(screen, rows, cols):
    gamestates = [[Cell(i,j) for i in range(rows)] for j in range(cols)]
    return gamestates

def event_checker(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit("Thanks for playing!")
        elif event.type == pygame.KEYDOWN:
            snake.get_move(event)

def main(ROWS, COLS):
    # Initialize Required Objects Start --------------------------------------------
    screen = initialize_pygame(600, 600)
    gamestates = initialize_gamestates(screen, ROWS, COLS)
    clock = pygame.time.Clock()
    snake = Snake(screen, gamestates)
    food = Food(gamestates, screen)
    # Initialize Required Objects End ---------------------------------------------
    while True:
        # Logic Handling Start ----------------------------------------------------
        snake.update_gamestates()
        food.eat_food(snake)
        event_checker(snake)
        snake.moves()
        snake.check_collisions()
        # Logic Handling End ------------------------------------------------------

        # Display Handling Start --------------------------------------------------
        screen.fill("white")
        food.spawn_food(snake)
        snake.draws()
        snake.display_score()
        pygame.display.flip()
        clock.tick(10)
        # Display Handling End ----------------------------------------------------

if __name__ == "__main__":
    main(20, 20)

