import pygame

class Button:
    def __init__(self, screen, x, y, width, height, color="white", text="testing"):
        #================ DIMENSION ATTRIBUTES =====================
        self.x_position = x
        self.y_position = y
        self.width = width
        self.height = height

        #================ DISPLAY ATTRIBUTES =======================
        self.screen = screen
        self.color = color
        self.text = text
        self.font_size = 12
        self.font = pygame.font.SysFont("comicsans", self.font_size)

    def display_button(self):
        button_text = self.font.render(self.text, True, "white")
        button_rect = pygame.Rect(self.x_position, self.y_position, self.width, self.height)
        self.screen.blit(button_text, button_rect)
        
    def check_pressed(self):
        pass
