import pygame
import spritesheet

class Player:
    def __init__(self):
        self.screen_width, self.screen_height = 800, 600
        self.animation_speed = 0.2

        # Running animation requirements
        self.run_sprites = spritesheet.SpriteSheet("Pink_Monster_Run_6.png")
        self.run_index = 0

        # Jump animation requirements
        self.jump_sprite = spritesheet.SpriteSheet("Pink_Monster_Jump_8.png")
        self.jump_index = 0

        # Initialize player dimensions
        self.player_height = 100
        self.player_width = 20

        # Initialize player position
        self.x_position = self.screen_width / 2
        self.y_position = self.screen_height - self.player_height

        # Initialize player velocities
        self.x_velocity = 0
        self.y_velocity = 0

        # Initialize player accelerations
        self.x_acceleration = 0
        self.y_acceleration = 0

        # Initialize player logic
        self.is_touching_ground = True
        self.direction = 1
        self.max_jumps = 2
        self.jump_count = 0

    def display_player(self, screen):
        player_rect = (self.x_position, self.y_position, self.player_width, self.player_height)
        self.animate_jump()

        # If Running use run sprites
        if self.y_velocity == 0 and self.is_touching_ground:
            frame_to_display = self.run_sprites.frame_list[int(self.run_index)]

        # If Jumping use jump sprites
        else:
            frame_to_display = self.jump_sprite.frame_list[int(self.jump_index)]

        # Flip frame if needed depending on player direction
        if self.direction < 0:
                frame_to_display = pygame.transform.flip(frame_to_display, True, False)


        screen.blit(frame_to_display, player_rect)

    def move_player(self):
        self.x_position += self.x_velocity
        self.y_position += self.y_velocity
        self.x_velocity += self.x_acceleration
        self.y_velocity += self.y_acceleration

    def get_player_movement(self, keys):
        if keys[pygame.K_LEFT]:
            self.x_velocity = -1
            self.direction = -1
            self.animate_run()
        elif keys[pygame.K_RIGHT]:
            self.x_velocity = 1
            self.direction = 1
            self.animate_run()
        else:
            self.x_velocity = 0

    def animate_run(self):
        if self.run_index <= self.run_sprites.number_of_animations - 1:
            self.run_index += self.animation_speed
        else:
            self.run_index = 0

    def animate_jump(self):
        # Reset jump animation if player touches the ground
        if self.is_touching_ground:
            self.jump_index = 0

        # Animate rising part of jump
        elif self.y_velocity < 0 and self.jump_index < 4:
            self.jump_index += self.animation_speed

        # Animate falling part of jump
        elif self.y_velocity > 0 and self.jump_index < self.jump_sprite.number_of_animations - 2:
            self.jump_index += self.animation_speed

    def jump_player(self):
        if self.jump_count < self.max_jumps:
            self.jump_count += 1
            self.y_velocity = -10

    def ground_check(self):
        if self.y_position > self.screen_height - self.player_height:
            self.is_touching_ground = True
            self.jump_count = 0
        else:
            self.is_touching_ground = False
