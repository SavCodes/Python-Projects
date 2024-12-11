import pygame
from PIL import Image, ImageTransform


class SpriteSheet:
    def __init__(self, sprite_sheet, scale=1.0, width=32, height=32):
        self.width = width
        self.height = height
        self.sprites = pygame.image.load(sprite_sheet)
        self.number_of_animations = int(sprite_sheet.split(".")[-2][-1])
        self.sprite_group = pygame.sprite.Group()
        self.scale = scale
        self.frame_list = [self.sprites.subsurface((self.width*index,0, self.width, self.height)) for index in range(self.number_of_animations)]
        self.frame_list = [pygame.transform.scale_by(frame, scale) for frame in self.frame_list]
        self.animation_index = 0
        self.animation_speed = 0.20

    def basic_animate(self, dampener=1):
        if self.animation_index < self.number_of_animations - 1:
            self.animation_index += self.animation_speed * dampener
        else:
            self.animation_index = 0

        return self.frame_list[int(self.animation_index)]

def generate_sway_sheet(file_path):
    # Load the original image_to_animate image
    image_to_animate = Image.open(file_path)

    # Create a list to store animation frames
    frames = []

    # Generate frames with transformations
    for angle in range(-10, 11, 5):  # Sway angles
        image_to_animate = image_to_animate.resize((64, 64))
        frame = image_to_animate.transform(image_to_animate.size, Image.Transform.AFFINE, (1, angle / 100, 0, 0, 1, 0))
        frames.append(frame)

    # Combine frames into a spritesheet
    width, height = image_to_animate.size
    spritesheet = Image.new("RGBA", (width * len(frames), height))

    for i, frame in enumerate(frames):
        spritesheet.paste(frame, (i * width, 0))

    # Save the spritesheet
    spritesheet.save(f"{file_path}_spritesheet_{len(frames)}.png")













