import pygame
import random
import time
import sys

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
        self.endIndex, self.currentIndex = self.arraySize, 0

    def displayArray(self):
        for index, rect in enumerate(self.array):
            if rect.isBeingSorted:
                color = (0, 255, 0)
            else:
                color = (255,255,255)
            rectangleDimensions = (index*self.rectWidth, self.screenHeight - rect.height, self.rectWidth, rect.height)
            pygame.draw.rect(self.screen, color, rectangleDimensions, width=0)

    def sortArray(self):
        self.array[self.currentIndex].isBeingSorted = True
        if self.endIndex == 0:
            time.sleep(5)
            sys.exit()
            
        # Once the full listed is sorted through return to the beginning and decrement the maximum index sorted
        if self.currentIndex >= self.endIndex - 1:
            self.array[self.currentIndex].isBeingSorted = False
            self.endIndex -= 1
            self.currentIndex = 0

        # If the current rectangle height is larger than the next rectangle's height, they swap positions
        if self.array[self.currentIndex].height > self.array[self.currentIndex+1].height:
            self.array[self.currentIndex], self.array[self.currentIndex+1] = self.array[self.currentIndex+1], self.array[self.currentIndex]

        self.displayArray()
        self.array[self.currentIndex].isBeingSorted = False
        self.currentIndex += 1


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
        clock.tick(60)  # limits FPS to 60
    pygame.quit()


if __name__ == '__main__':
    main()
