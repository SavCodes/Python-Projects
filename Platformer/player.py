import pygame
import spritesheet

# Dead players still linger in memory => Find a way to remove instantiated player object

class Player:
    def __init__(self):
        self.screen_width, self.screen_height = 800, 600
        self.animation_speed = 0.2

        # Idle animation requirements
        self.idle_sprites = spritesheet.SpriteSheet("Pink_Monster_Idle_4.png")
        self.idle_index = 0
        self.is_attacking = False

        # Death animation requirements
        self.death_sprites = spritesheet.SpriteSheet("Pink_Monster_Death_8.png")
        self.death_index = 0
        self.is_alive = True
        self.max_health = 100
        self.current_health = self.max_health

        # Walking animation requirements
        self.walk_sprites = spritesheet.SpriteSheet("Pink_Monster_Walk_6.png")
        self.walk_index = 0

        # Running animation requirements
        self.run_sprites = spritesheet.SpriteSheet("Pink_Monster_Run_6.png")
        self.run_index = 0

        # Jump animation requirements
        self.jump_sprites = spritesheet.SpriteSheet("Pink_Monster_Jump_8.png")
        self.jump_index = 0
        self.max_jumps = 2
        self.jump_count = 0
        self.is_touching_ground = True

        # Double jump animation requirements
        self.double_jump_sprites = spritesheet.SpriteSheet("Double_Jump_Dust_5.png")
        self.double_jump_index = 0

        # Attack animation requirements
        self.attack_sprites = spritesheet.SpriteSheet("Pink_Monster_Attack1_4.png")
        self.attack_index = 0

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
        self.direction = 1

    def display_player(self, screen):
        player_rect = (self.x_position, self.y_position, self.player_width, self.player_height)
        self.animate_idle()
        self.animate_jump()
        self.animate_walk()
        self.animate_run()
        self.animate_attack()
        self.animate_death()

        # If the player died play the death animation:
        if self.current_health <= 0:
            frame_to_display = self.death_sprites.frame_list[int(self.death_index)]

        # If attacking use attack animation
        elif self.is_attacking:
            frame_to_display = self.attack_sprites.frame_list[int(self.attack_index)]

        # If Standing use idle sprites
        elif self.x_velocity == 0 and self.is_touching_ground:
            frame_to_display = self.idle_sprites.frame_list[int(self.idle_index)]

        # If Walking use walk sprites
        elif self.y_velocity == 0 and self.is_touching_ground and abs(self.x_velocity) < 3:
            frame_to_display = self.walk_sprites.frame_list[int(self.walk_index)]

        # If Running use run sprites
        elif self.y_velocity == 0 and self.is_touching_ground:
            frame_to_display = self.run_sprites.frame_list[int(self.run_index)]

        # If Jumping use jump sprites
        else:
            frame_to_display = self.jump_sprites.frame_list[int(self.jump_index)]

        # Flip frame if needed depending on player direction
        if self.direction < 0:
            frame_to_display = pygame.transform.flip(frame_to_display, True, False)

        if self.is_alive:
            screen.blit(frame_to_display, player_rect)

    def move_player(self):
        self.x_position += self.x_velocity
        self.y_position += self.y_velocity
        self.x_velocity += self.x_acceleration
        self.y_velocity += self.y_acceleration

    def get_player_movement(self, keys):
        if keys[pygame.K_1] and keys[pygame.K_LEFT]:
            self.x_velocity = -3
            self.direction = -1

        elif keys[pygame.K_1] and keys[pygame.K_RIGHT]:
            self.x_velocity = 3
            self.direction = 1

        elif keys[pygame.K_LEFT]:
            self.x_velocity = -1
            self.direction = -1

        elif keys[pygame.K_RIGHT]:
            self.x_velocity = 1
            self.direction = 1

        else:
            self.x_velocity = 0

    def animate_idle(self, dampener=0.5):
        if self.x_velocity == 0 and self.idle_index < self.idle_sprites.number_of_animations - 1:
            self.idle_index += self.animation_speed * dampener
        else:
            self.idle_index = 0

    def animate_walk(self):
        if self.walk_index <= self.walk_sprites.number_of_animations - 1:
            self.walk_index += self.animation_speed
        else:
            self.walk_index = 0

    def animate_run(self):
        if self.run_index < self.run_sprites.number_of_animations - 1:
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
        elif self.y_velocity > 0 and self.jump_index < self.jump_sprites.number_of_animations - 2:
            self.jump_index += self.animation_speed

    def animate_double_jump(self):
        if self.jump_index == 2 and self.double_jump_index < self.double_jump_sprites.number_of_animations - 1:
            self.double_jump_index += self.animation_speed

        if self.double_jump_index == self.double_jump_sprites.number_of_animations:
            pass

    def animate_death(self):
        if self.current_health == 0 and self.death_index < self.death_sprites.number_of_animations - 1:
            self.death_index += self.animation_speed

        elif self.current_health == 0 and self.death_index >= self.death_sprites.number_of_animations -1:
            self.is_alive = False

        else:
            self.death_index = 0

    def animate_attack(self):
        if self.is_attacking and self.attack_index < self.attack_sprites.number_of_animations - 1:
            self.attack_index += self.animation_speed
        else:
            self.is_attacking = False
            self.attack_index = 0

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

    def player_event_checker(self, game_event):
        if game_event.type == pygame.KEYDOWN and game_event.key == pygame.K_SPACE:
            self.jump_player()

        elif game_event.type == pygame.KEYDOWN and game_event.key == pygame.K_q and not self.is_attacking:
            self.is_attacking = True

        elif game_event.type == pygame.KEYDOWN and game_event.key == pygame.K_ESCAPE:
            self.current_health -= 100

        elif game_event.type == pygame.KEYDOWN and game_event.key == pygame.K_TAB:
            self.current_health = self.max_health
            self.is_alive = True

        keys = pygame.key.get_pressed()
        self.get_player_movement(keys)
