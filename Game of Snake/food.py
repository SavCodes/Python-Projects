import random
import pygame

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
