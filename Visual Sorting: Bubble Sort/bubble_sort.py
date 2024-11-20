import pygame
import random

class BubbleSorter:
    def __init__(self, arraySize):
        self.screen = pygame.display.set_mode((600, 600))
        self.arraySize = arraySize
        self.screenWidth, self.screenHeight = self.screen.get_size()
        self.rectWidth = self.screenWidth / self.arraySize
        self.array = [random.randint(1,100) for i in range(self.arraySize)]

    def displayArray(self):
        for index, rectHeight in enumerate(self.array):
            rectangleDimensions = (index*self.rectWidth, self.screenHeight - rectHeight, self.rectWidth, rectHeight)
            pygame.draw.rect(self.screen, (255,255,255), rectangleDimensions, width=0)

    def sortArray(self):
        pass

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True
    bubbleSorter = BubbleSorter(100)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("purple")
        bubbleSorter.displayArray()
        pygame.display.flip()
        clock.tick(60)  # limits FPS to 60
    pygame.quit()


if __name__ == '__main__':
    main()
