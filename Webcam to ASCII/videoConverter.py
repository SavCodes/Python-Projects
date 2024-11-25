import cv2
import pygame

def map_brightness_to_ascii(brightness):
    # Density map for converting pixel
    color_map = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    # Reverses color map to match darker pixels to characters with more open space
    negative_color_map = color_map[::-1]
    # Create indexing for accessing right character from the color map
    interval = 255 / (len(color_map)-1)
    map_index = int(brightness // interval)
    # Retrieve ascii character corresponding to pixel brightness
    new_text = negative_color_map[map_index]
    return new_text

def format_ascii_image(ascii_image):
    formatted_ascii_image = []
    for row in ascii_image:
        ascii_row = ""
        for character in row:
            ascii_row += character
        formatted_ascii_image.append(ascii_row)
    return formatted_ascii_image

def initialize_pygame():
    pygame.init()
    pygame.display.set_caption("VIDEO TO ASCII")
    return pygame.display.set_mode((900, 700))

def display_image(formatted_ascii_image, screen):
    text_size = 2
    font = pygame.font.SysFont("Courier New", text_size)
    for ind, line in enumerate(formatted_ascii_image):
        text = font.render(line, True, (255, 255, 255))
        text_box = text.get_rect(y=ind * text_size)
        screen.blit(text, text_box)

def event_checker():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True

# Load the video
video = cv2.VideoCapture(0)

# Initialize pygame
screen = initialize_pygame()

running = True
while running:
    # Check for input to close window
    running = event_checker()

    # Read in video data and turn it to gray scale
    ret, frame = video.read()
    frame = cv2.resize(frame, (500, 500))
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert pixels to ascii character based on brightness value
    ascii_image = [[map_brightness_to_ascii(pixel) for pixel in row] for row in gray_frame]

    # Format image for display processing
    formatted_image = format_ascii_image(ascii_image)

    # Display formatted image via pygame
    screen.fill((0, 0, 0))
    display_image(formatted_image, screen)
    pygame.display.update()
