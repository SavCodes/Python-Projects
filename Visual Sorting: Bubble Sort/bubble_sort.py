import pygame
import random
import time

# TO DO LIST:
# -Add a sound effect corresponding to the height of the rectangle

class Rectangle:
    def __init__(self, height):
        self.height = height
        self.isBeingSorted = False

class BubbleSorter:
    def __init__(self, array_size):
        self.clock = Clock()
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
        # Sets font and font size for all text displayed to screen
        text_size = 25
        font = pygame.font.Font(None, text_size)
        # Generate the title text
        title_text = font.render("Bubble Sorter", True, (0, 0, 0))
        title_text_pos = title_text.get_rect(centerx=self.arraySize/2 * self.rectWidth)
        # Generates the running total of comparisons performed while sorting
        array_size_text = font.render(f"Array Size: {self.arraySize}" , True, (10, 10, 10))
        array_size_pos = array_size_text.get_rect(x=0, y=0)
        # Generates the running total of comparisons performed while sorting
        count_text = font.render(f"Comparisons: {self.comparisonCount}" , True, (10, 10, 10))
        count_text_pos = count_text.get_rect(x=0, y=text_size//2 + 1)
        # Generates the running total of rectangle swaps performed while sorting
        swap_text = font.render(f"Swaps: {self.swapCount}" , True, (10, 10, 10))
        swap_text_pos = count_text.get_rect(x=0, y=text_size + 2)
        # Displays both the comparison and swap count to screen
        self.screen.blit(title_text, title_text_pos)
        self.screen.blit(array_size_text, array_size_pos)
        self.screen.blit(swap_text, swap_text_pos)
        self.screen.blit(count_text, count_text_pos)

    def restart_array(self):
        time.sleep(2)
        self.clock.current_time = 0
        self.comparisonCount, self.swapCount = 0, 0
        self.array = [Rectangle(random.randint(1,self.screenHeight)) for i in range(self.arraySize)]

class Clock:
    def __init__(self, tick_speed=300):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((600, 600))
        self.current_time = 0
        self.text_size = 25
        self.tick_speed = tick_speed
        self.screen_height, self.screen_width = pygame.display.get_window_size()
        self.font = pygame.font.Font(None, self.text_size)

    def update(self):
        self.clock.tick(self.tick_speed)
        self.current_time += self.clock.get_time()

    def display(self):
        clock_text = self.font.render(f"Time: {self.current_time/1000:.2f}s", True, (0, 0, 0))
        clock_text_position = clock_text.get_rect(x=0, y=self.text_size / 2 * 3 + 3)
        self.screen.blit(clock_text, clock_text_position)

def event_checker():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True

def initialize_pygame():
    pygame.init()
    pygame.display.set_caption("Bubble Sorter")
    pygame.display.set_icon(pygame.image.load('bubble.jfif'))
    screen = pygame.display.set_mode((600, 600))
    return screen

def main(rectangle_number):
    running = True
    screen= initialize_pygame()
    bubbleSorter = BubbleSorter(rectangle_number)
    while running:
        running = event_checker()
        bubbleSorter.screen.fill((50, 50, 50))
        bubbleSorter.sort_array()
        bubbleSorter.display_statistics()
        bubbleSorter.clock.update()
        bubbleSorter.clock.display()
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main(rectangle_number=50)
