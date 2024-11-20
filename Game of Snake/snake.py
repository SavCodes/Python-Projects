import pygame
import pygame_widgets
import random
import sys
import time
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

# TO DO LIST:
#      - Add grid pattern to board
#      - Add an endless mode option
#      - Add Highscore Leaderboard
#      - Make "Game Paused" and "Start Game" bob up and down

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

def event_checker(snake, is_paused):
    # Valid moves to change the direction of the snake
    move_set = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN,
                pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a]

    # Handles all events in the game loop
    events = pygame.event.get()
    for event in events:
        # Exits game is the program is closed
        if event.type == pygame.QUIT:
            sys.exit("Thanks for playing!")
        # Logic for handling pressed keys
        elif event.type == pygame.KEYDOWN:
            # Logic for pausing/unpausing game
            if event.key == pygame.K_SPACE:
                is_paused = not is_paused
            # Logic for updating snake movement direction
            elif event.key in move_set:
                snake.get_move(event)
    pygame_widgets.update(events)
    return is_paused

def initialize_slider(screen):
    width, height = pygame.display.get_window_size()
    txt_scl = 50
    slider = Slider(screen, width // 4, height - txt_scl, width//2, 20, min=1, max=3, step=1)
    output = TextBox(screen, width // 2 - txt_scl // 2 , height - txt_scl // 2, txt_scl //2 , txt_scl//2, fontSize=10)
    output.disable()  # Act as label instead of textbox
    return slider, output

def draw_slider(slider, output):
    events = pygame.event.get()
    output.setText(f"Difficulty: {slider.getValue()}")
    pygame_widgets.update(events)

def display_pause_menu(screen):
    # Initialized display associated variables
    width, height = pygame.display.get_window_size()

    # Displays "Game Paused!" Start --------------------------------------------
    pause_text = "Game Paused!"
    pause_size = width // 8
    my_font = pygame.font.SysFont('Comic Sans MS', pause_size)
    pause_surface = my_font.render(pause_text, True, "black")
    pause_rect = pause_surface.get_rect(center=(width//2, height//2))
    screen.blit(pause_surface, pause_rect)
    # Display "Game Pause!" End ------------------------------------------------

    # Displays Pause Instructions Start ----------------------------------------
    instructions_text = "Press Space to Pause/Unpause"
    instructions_size = width // 20
    my_font = pygame.font.SysFont('Comic Sans MS', instructions_size)
    instruction_surface = my_font.render(instructions_text, True, "black")
    instruction_rect = instruction_surface.get_rect(center=(width//2,  height * 0.7))
    screen.blit(instruction_surface, instruction_rect)
    # Display Pause Instructions End -------------------------------------------

    # Displays Move Instructions Start -----------------------------------------
    move_instructions_text = "Use the arrow keys or w, a, s, d to move"
    move_instructions_size = width // 20
    my_font = pygame.font.SysFont('Comic Sans MS', move_instructions_size)
    move_instruction_surface = my_font.render(move_instructions_text, True, "black")
    move_instruction_rect = move_instruction_surface.get_rect(center=(width//2, height * 0.8))
    screen.blit(move_instruction_surface, move_instruction_rect)
    # Display Move Instructions End --------------------------------------------

def main(ROWS, COLS):
    # Initialize Required Objects Start -------------------------------------------
    screen = initialize_pygame(600, 600)
    gamestates = initialize_gamestates(screen, ROWS, COLS)
    slider, output = initialize_slider(screen)
    clock = pygame.time.Clock()
    snake = Snake(screen, gamestates)
    food = Food(gamestates, screen)
    is_paused = True
    # Initialize Required Objects End ---------------------------------------------

    while True:
        is_paused = event_checker(snake, is_paused)
        screen.fill("white")
        if not is_paused:
            # Logic Handling Start ----------------------------------------------------
            snake.update_gamestates()
            food.eat_food(snake)
            snake.moves()
            snake.check_collisions()
            # Logic Handling End ------------------------------------------------------

            # Display Handling Start --------------------------------------------------
            food.spawn_food(snake)
            snake.draws()
            snake.display_score()
            pygame.display.flip()
            clock.tick(slider.getValue() * 5)
            # Display Handling End ----------------------------------------------------
        else:
            # Pause Menu Start --------------------------------------------------------
            draw_slider(slider, output)
            display_pause_menu(screen)
            pygame.display.update()
            # Pause Menu End ----------------------------------------------------------\

if __name__ == "__main__":
    main(20, 20)


