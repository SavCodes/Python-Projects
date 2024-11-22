import pygame
import random
import time

class Rectangle:
    def __init__(self, height):
        self.height = height
        self.isBeingSorted = False
        self.isSorted = False

class InsertionSorter:
    def __init__(self, array_size):
        self.clock = Clock()
        self.screen = pygame.display.set_mode((600, 600))
        self.arraySize = array_size
        self.screenWidth, self.screenHeight = self.screen.get_size()
        self.rectWidth = self.screenWidth / self.arraySize
        self.array = [Rectangle(random.randint(1,self.screenHeight)) for i in range(self.arraySize)]
        self.resumeIndex, self.currentIndex = 1, 1
        self.comparisonCount, self.swapCount = 0, 0
        self.display_array()
        self.array[0].isSorted = True

    def display_array(self):
        for index, rect in enumerate(self.array):
            if rect.isBeingSorted:
                color = (255, 00, 0)
            elif rect.isSorted:
                color = (0, 255, 0)
            else:
                color = (255,255,255)
            rectangleDimensions = (index*self.rectWidth+1, self.screenHeight - rect.height+1, self.rectWidth-1, rect.height)
            borderDimensions = (index * self.rectWidth, self.screenHeight - rect.height, self.rectWidth, rect.height)
            pygame.draw.rect(self.screen, "black", borderDimensions, width=0)
            pygame.draw.rect(self.screen, color, rectangleDimensions, width=0)

    def check_done_sorting(self):
        if self.resumeIndex > len(self.array) + 1 or self.currentIndex == len(self.array):
            self.currentIndex, self.resumeIndex = 1, 1
            self.restart_array()

    def loop_through_rectangles(self):
        if self.currentIndex == 0:
            self.array[self.currentIndex].isBeingSorted = False
            self.array[self.currentIndex].isSorted = True
            self.resumeIndex += 1
            self.currentIndex = self.resumeIndex

    def compare_and_swap(self):
        if self.array[self.currentIndex].height < self.array[self.currentIndex-1].height:
            self.array[self.currentIndex], self.array[self.currentIndex-1] = self.array[self.currentIndex-1], self.array[self.currentIndex]
            self.array[self.currentIndex-1].isBeingSorted = True
            self.array[self.currentIndex].isBeingSorted = False
            self.swapCount += 1
            self.currentIndex -= 1

        else:
            self.array[self.currentIndex].isSorted = True
            self.array[self.currentIndex].isBeingSorted = False
            self.resumeIndex += 1
            self.currentIndex = self.resumeIndex

    def sort_array(self):
        # Display the updated rectangle states
        self.display_array()
        # Once the full array of rectangles is sorted exit the program
        self.check_done_sorting()
        # Keeps track of statistics related to sorting
        self.comparisonCount += 1
        # Once the rectangle is fully sorted, return to the beginning and decrement the maximum index sorted
        self.loop_through_rectangles()
        # If the current rectangle height is larger than the next rectangle's height, they swap positions
        self.compare_and_swap()

    def display_statistics(self):
        # Sets font and font size for all text displayed to screen
        text_size = 25
        font = pygame.font.Font(None, text_size)
        # Generate the title text
        title_text = font.render("Insertion Sort Visualization", True, (0, 0, 0))
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
        self.array[0].isSorted = True

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
    pygame.display.set_caption("Insertion Sorter")
    #pygame.display.set_icon(pygame.image.load('bubble.jfif'))
    screen = pygame.display.set_mode((600, 600))
    return screen

def main(rectangle_number):
    running = True
    screen= initialize_pygame()
    insertion_sorter = InsertionSorter(rectangle_number)
    while running:
        running = event_checker()
        insertion_sorter.screen.fill((50, 50, 50))
        insertion_sorter.sort_array()
        insertion_sorter.display_statistics()
        insertion_sorter.clock.update()
        insertion_sorter.clock.display()
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main(rectangle_number=50)
