import cv2
import pygame

pygame.init()
screen = pygame.display.set_mode((600,600))

def map_brightness_to_ascii(brightness):
    color_map = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    negative_color_map = color_map[::-1]
    interval = 255 / (len(color_map)-1)
    map_index = int(brightness // interval)
    new_text = negative_color_map[map_index]
    return new_text

def load_image():
    image = cv2.imread('img.png', cv2.IMREAD_GRAYSCALE)
    resized_image = cv2.resize(image, (50,50))
    full_ascii = []
    for row in resized_image:
        row_chars = ""
        for pixel in row:
            ascii_character = map_brightness_to_ascii(pixel)
            row_chars += ascii_character
        full_ascii.append(row_chars)
    return full_ascii

def event_checker():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True

def display_text(converted_image, screen):
    text_size = 10
    font = pygame.font.SysFont("Courier New", text_size)
    for i, line in enumerate(converted_image):
        text = font.render(line, True, (255,255,255))
        text_box = text.get_rect(y=i*text_size)
        screen.blit(text, text_box)

def main():
    full_ascii = load_image()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((600,600))
    running = True
    while running:
        running = event_checker()
        display_text(full_ascii, screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
