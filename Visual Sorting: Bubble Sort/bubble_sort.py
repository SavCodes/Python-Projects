import pygame
import random
import time
import sys

# TO DO LIST:
# -Add running statistics display (total number of comparisons, number of swaps, total time to run)
# -Add title text "Bubble Sort"
# -Add program logo and caption
# -Add a round corresponding to the height of the rectangle

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
        self.array = [Rectangle(random.randint(1,self.screenHeight)) for i in range(self.arraySize)]
        self.endIndex, self.currentIndex = self.arraySize, 0
        self.comparisonCount, self.swapCount = 0, 0

    def displayArray(self):
        for index, rect in enumerate(self.array):
            if rect.isBeingSorted:
                color = (0, 255, 0)
            else:
                color = (255,255,255)
            rectangleDimensions = (index*self.rectWidth, self.screenHeight - rect.height, self.rectWidth, rect.height)
            pygame.draw.rect(self.screen, color, rectangleDimensions, width=0)

    def checkDoneSorting(self):
        if self.endIndex == 0:
            print(f"Comparison: {self.comparisonCount}    ||    Swaps: {self.swapCount}")
            time.sleep(5)
            sys.exit()

    def loopThroughRectangles(self):
        if self.currentIndex >= self.endIndex - 1:
            self.array[self.currentIndex].isBeingSorted = False
            self.endIndex -= 1
            self.currentIndex = 0

    def compareAndSwap(self):
        if self.array[self.currentIndex].height > self.array[self.currentIndex+1].height:
            self.swapCount += 1
            self.array[self.currentIndex], self.array[self.currentIndex+1] = self.array[self.currentIndex+1], self.array[self.currentIndex]

    def sortArray(self):
        # Keeps track of statistics related to sorting
        self.comparisonCount += 1
        # Update sort state of rectangle to active
        self.array[self.currentIndex].isBeingSorted = True
        # Once the full array of rectangles is sorted exit the program
        self.checkDoneSorting()
        # Once the rectangle is fully sorted, return to the beginning and decrement the maximum index sorted
        self.loopThroughRectangles()
        # If the current rectangle height is larger than the next rectangle's height, they swap positions
        self.compareAndSwap()
        # Display the updated rectangle states
        self.displayArray()
        # Update sort status of rectangle to inactive
        self.array[self.currentIndex].isBeingSorted = False
        # Increment to next rectangle comparison
        self.currentIndex += 1

    def display_statistics(self):
        pass

def main(rectangleNumber):
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True
    bubbleSorter = BubbleSorter(rectangleNumber)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("purple")
        bubbleSorter.sortArray()
        bubbleSorter.display_statistics()
        pygame.display.flip()
        clock.tick(300)  # limits FPS to 60
    pygame.quit()

if __name__ == '__main__':
    main(rectangleNumber=100)
