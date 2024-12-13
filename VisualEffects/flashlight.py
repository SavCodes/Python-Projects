import pygame
from pygame import BLEND_RGBA_ADD

MAX_SIZE = 200

class Flashlight:
    def __init__(self, screen, x, y, size=5):
        self.x = x
        self.y = y
        self.screen = screen
        self.size = size
        self.color = 2

    def draw(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        circle_surface = pygame.Surface((2*self.size, 4*self.size))
        pygame.draw.circle(circle_surface, (self.color,self.color,self.color), (self.size,2*self.size), self.size)
        self.screen.blit(circle_surface,circle_surface.get_rect(center=(mouse_x,mouse_y)), special_flags=BLEND_RGBA_ADD)

    def grow(self):
        self.size *= 1


def event_checker():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True

def main():
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    flashlight = [Flashlight(screen, mouse_x, mouse_y, MAX_SIZE - i) for i in range(100)]

    running = True

    while running:
        running = event_checker()
        pygame.draw.rect(screen, (100,0,0), (0, 0, 800, 600))
        pygame.draw.rect(screen, (0,100,0), (400, 0, 800, 600))

        for light in flashlight:
            light.draw()

        pygame.display.update()
        clock.tick(60)
    pygame.quit()


main()
