import pygame
import random
import time
import sys

# TO DO LIST:
# -Add running statistics display (total number of comparisons, number of swaps, total time to run)
# -Add title text "Bubble Sort"
# -Add program logo and caption
# -Add a sound effect corresponding to the height of the rectangle

class Rectangle:
    def __init__(self, height):
        self.height = height
        self.isBeingSorted = False

class BubbleSorter:
    def __init__(self, array_size):
        self.screen = pygame.display.set_mode((600, 600))
        self.arraySize = array_size
        self.screenWidth, self.screenHeight = self.screen.get_size()
        self.rectWidth = self.screenWidth / self.arraySize
        self.array = [Rectangle(random.randint(1,self.screenHeight)) for i in range(self.arraySize)]
        self.endIndex, self.currentIndex = self.arraySize, 0
        self.comparisonCount, self.swapCount = 0, 0

    def display_array(self):
        for index, rect in enumerate(self.array):
            if rect.isBeingSorted:
                color = (0, 255, 0)
            else:
                color = (255,255,255)
            rectangleDimensions = (index*self.rectWidth+1, self.screenHeight - rect.height+1, self.rectWidth-1, rect.height)
            borderDimensions = (index * self.rectWidth, self.screenHeight - rect.height, self.rectWidth, rect.height)
            pygame.draw.rect(self.screen, "black", borderDimensions, width=0)
            pygame.draw.rect(self.screen, color, rectangleDimensions, width=0)

    def check_done_sorting(self):
        if self.endIndex == 0:
            print(f"Comparison: {self.comparisonCount}    ||    Swaps: {self.swapCount}")
            self.currentIndex, self.endIndex = 0, len(self.array)
            self.restart_array()

    def loop_through_rectangles(self):
        if self.currentIndex >= self.endIndex - 1:
            self.array[self.currentIndex].isBeingSorted = False
            self.endIndex -= 1
            self.currentIndex = 0

    def compare_and_swap(self):
        if self.array[self.currentIndex].height > self.array[self.currentIndex+1].height:
            self.swapCount += 1
            self.array[self.currentIndex], self.array[self.currentIndex+1] = self.array[self.currentIndex+1], self.array[self.currentIndex]

    def sort_array(self):
        # Keeps track of statistics related to sorting
        self.comparisonCount += 1
        # Update sort state of rectangle to active
        self.array[self.currentIndex].isBeingSorted = True
        # Display the updated rectangle states
        self.display_array()
        # Once the full array of rectangles is sorted exit the program
        self.check_done_sorting()
        # Once the rectangle is fully sorted, return to the beginning and decrement the maximum index sorted
        self.loop_through_rectangles()
        # If the current rectangle height is larger than the next rectangle's height, they swap positions
        self.compare_and_swap()
        # Update sort status of rectangle to inactive
        self.array[self.currentIndex].isBeingSorted = False
        # Increment to next rectangle comparison
        self.currentIndex += 1

    def display_statistics(self):
        textSize = 25
        font = pygame.font.Font(None, textSize)
        countText = font.render(f"Comparisons: {self.comparisonCount}" , True, (10, 10, 10))
        countTextPos = countText.get_rect(x=0, y=0)
        swapText = font.render(f"Swaps: {self.swapCount}" , True, (10, 10, 10))
        swapTextPos = countText.get_rect(x=0, y=textSize/2)
        self.screen.blit(swapText, swapTextPos)
        self.screen.blit(countText, countTextPos)

    def restart_array(self):
        time.sleep(2)
        self.comparisonCount, self.swapCount = 0, 0
        self.array = [Rectangle(random.randint(1,self.screenHeight)) for i in range(self.arraySize)]

def main(rectangle_number):
    pygame.init()
    pygame.display.set_caption("Bubble Sorter")

    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_icon(pygame.image.load('bubble.jfif'))
    clock = pygame.time.Clock()
    running = True
    bubbleSorter = BubbleSorter(rectangle_number)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("purple")
        bubbleSorter.sort_array()
        bubbleSorter.display_statistics()
        pygame.display.flip()
        clock.tick(5)  # limits FPS to 60
    pygame.quit()

if __name__ == '__main__':
    main(rectangle_number=10)
