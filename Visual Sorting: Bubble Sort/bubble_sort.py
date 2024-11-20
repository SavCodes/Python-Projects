import pygame
import random

class Rectangle:
    def __init__(self, height):
        self.height = height
        self.isBeingSorted = False

class BubbleSorter:
    def __init__(self, arraySize):
        self.screen = pygame.display.set_mode((600, 600))
        self.arraySize = arraySize
        self.screenWidth, self.screenHeight = self.screen.get_size()
        self.rectWidth = self.screenWidth / self.arraySize
        self.array = [Rectangle(random.randint(1,100)) for i in range(self.arraySize)]
        self.startIndex, self.currentIndex = 0, 0

    def displayArray(self):
        for index, rect in enumerate(self.array):
            if rect.isBeingSorted:
                color = (0, 255, 0)
            else:
                color = (255,255,255)
            rectangleDimensions = (index*self.rectWidth, self.screenHeight - rect.height, self.rectWidth, rect.height)
            pygame.draw.rect(self.screen, color, rectangleDimensions, width=0)

    def sortArray(self):
        # Checks current rectangle in the array against the next, if it is larger they swap
        if self.currentIndex >= len(self.array) - 1:
            self.currentIndex = 0

        if self.array[self.currentIndex].height > self.array[self.currentIndex+1].height:
            self.array[self.currentIndex], self.array[self.currentIndex+1] = self.array[self.currentIndex+1], self.array[self.currentIndex]

        self.currentIndex += 1
        self.displayArray()


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True
    bubbleSorter = BubbleSorter(30)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("purple")
        bubbleSorter.sortArray()
        pygame.display.flip()
        clock.tick(120)  # limits FPS to 60
    pygame.quit()


if __name__ == '__main__':
    main()
