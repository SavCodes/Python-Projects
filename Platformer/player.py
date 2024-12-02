import pygame
import spritesheet

# Optimize Collision check by isolating and only checking tiles that are within reach

class Player:
    def __init__(self,scale=1, arrow_controls=True):
        self.screen_width, self.screen_height = 800, 600
        self.image = None
        self.animation_speed = 0.2
        self.scale = scale
        self.character_image_directory = "./game_assets/player_spritesheets/"

        # Idle animation requirements
        self.idle_sprites = spritesheet.SpriteSheet(self.character_image_directory + "Idle_4.png", scale=self.scale)
        self.idle_index = 0
        self.is_attacking = False
        self.idle_inhale = True

        # Death animation requirements
        self.death_sprites = spritesheet.SpriteSheet(self.character_image_directory+ "Death_8.png", scale=self.scale)
        self.death_index = 0
        self.is_alive = True
        self.max_health = 100
        self.current_health = self.max_health

        # Walking animation requirements
        self.walk_sprites = spritesheet.SpriteSheet(self.character_image_directory + "Walk_6.png", scale=self.scale)
        self.walk_index = 0

        # Running animation requirements
        self.run_sprites = spritesheet.SpriteSheet(self.character_image_directory + "Run_6.png", scale=self.scale)
        self.run_index = 0

        # Jump animation requirements
        self.jump_sprites = spritesheet.SpriteSheet(self.character_image_directory + "Jump_8.png", scale=self.scale)
        self.jump_index = 0
        self.max_jumps = 2
        self.jump_count = 0
        self.is_touching_ground = False

        # Double jump animation requirements
        self.double_jump_sprites = spritesheet.SpriteSheet(self.character_image_directory + "Double_Jump_Dust_5.png", scale=self.scale)
        self.double_jump_index = 0

        # Attack animation requirements
        self.attack_sprites = spritesheet.SpriteSheet(self.character_image_directory + "Attack1_4.png", scale=self.scale)
        self.attack_index = 0

        # Initialize player position
        self.x_position = self.screen_width / 2
        self.y_position = self.screen_height // 2

        # Initialize player dimensions
        self.player_height = 32 * self.scale
        self.player_width = 32 * self.scale
        self.player_width_buffer = 32 * self.scale * 0.2

        # Initialize player velocities
        self.x_velocity = 0
        self.y_velocity = 0

        # Initialize player accelerations
        self.x_acceleration = 0
        self.y_acceleration = 0

        # Initialize player logic
        self.direction = 1
        self.collision_direction = None
        self.collision = False
        self.arrow_controls = arrow_controls

    def display_player(self, screen):
        self.player_rect = (self.x_position, self.y_position, self.player_width, self.player_height)
        self.animate_double_jump(screen)

        # If the player died play the death animation:
        if self.current_health <= 0:
            frame_to_display = self.animate_death()

        # If attacking use attack animation
        elif self.is_attacking:
            frame_to_display = self.animate_attack()

        # If Standing use idle sprites
        elif self.x_velocity == 0 and self.is_touching_ground:
            frame_to_display = self.animate_idle()

        # If Walking use walk sprites
        elif self.y_velocity == 0 and self.is_touching_ground and abs(self.x_velocity) < 3:
            frame_to_display = self.animate_walk()

        # If Running use run sprites
        elif self.y_velocity == 0 and self.is_touching_ground:
            frame_to_display = self.animate_run()

        # If Jumping use jump sprites
        else:
            frame_to_display = self.animate_jump()

        # Flip frame if needed depending on player direction
        if self.direction < 0:
            frame_to_display = pygame.transform.flip(frame_to_display, True, False)

        if self.is_alive:
            screen.blit(frame_to_display, self.player_rect)

        self.image = frame_to_display

    def move_player(self, walls):
        self.x_position += self.x_velocity
        self.y_position += self.y_velocity
        self.x_velocity += self.x_acceleration
        self.y_velocity += self.y_acceleration
        self.resolve_collision(walls)

    def get_player_movement(self, keys):
        if self.arrow_controls:
            controls = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        else:
            controls = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]

        # Sprint left
        if keys[pygame.K_1] and keys[controls[0]]:
            self.x_velocity = -3
            self.direction = -1

        # Sprint right
        elif keys[pygame.K_1] and keys[controls[1]]:
            self.x_velocity = 3
            self.direction = 1

        # Walk left
        elif keys[controls[0]]:
            self.x_velocity = -1
            self.direction = -1

        # Walk right
        elif keys[controls[1]]:
            self.x_velocity = 1
            self.direction = 1

        else:
            self.x_velocity = 0

    def animate_idle(self, dampener=0.5):
        if int(self.idle_index) == self.idle_sprites.number_of_animations - 1:
            self. idle_inhale = False

        if self.x_velocity == 0 and self.idle_inhale and self.idle_index < self.idle_sprites.number_of_animations - 1:
            self.idle_index += self.animation_speed * dampener

        elif self.x_velocity == 0 and not self.idle_inhale and self.idle_index > 0 + self.animation_speed:
            self.idle_index -= self.animation_speed * dampener

        else:
            self.idle_inhale = True
            self.idle_index = 0

        return self.idle_sprites.frame_list[int(self.idle_index)]

    def animate_walk(self):
        if self.walk_index <= self.walk_sprites.number_of_animations - 1:
            self.walk_index += self.animation_speed
        else:
            self.walk_index = 0

        return self.walk_sprites.frame_list[int(self.walk_index)]

    def animate_run(self):
        if self.run_index < self.run_sprites.number_of_animations - 1:
            self.run_index += self.animation_speed
        else:
            self.run_index = 0

        return self.run_sprites.frame_list[int(self.run_index)]

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

        return self.jump_sprites.frame_list[int(self.jump_index)]

    def animate_double_jump(self, screen):
        if self.jump_count == 2 and self.double_jump_index < self.double_jump_sprites.number_of_animations - 1:
            double_jump_dust_surface = (self.x_position, self.y_position + self.player_height // 6, self.player_width, self.player_height)
            screen.blit(self.double_jump_sprites.frame_list[int(self.double_jump_index)], double_jump_dust_surface)
            self.double_jump_index += self.animation_speed
        if self.jump_count == 0:
            self.double_jump_index = 0

    def animate_death(self):
        if self.current_health <= 0 and self.death_index < self.death_sprites.number_of_animations - 1 and self.is_alive:
            self.death_index += self.animation_speed

        elif self.current_health <= 0 and self.death_index > self.death_sprites.number_of_animations -1:
            self.is_alive = False
            self.death_index = 0

        return self.death_sprites.frame_list[int(self.death_index)]

    def animate_attack(self):
        if self.is_attacking and self.attack_index < self.attack_sprites.number_of_animations - 1:
            self.attack_index += self.animation_speed
        else:
            self.is_attacking = False
            self.attack_index = 0

        return self.attack_sprites.frame_list[int(self.attack_index)]

    def jump_player(self):
        self.is_touching_ground = False
        if self.jump_count < self.max_jumps:
            self.jump_count += 1
            self.y_velocity = -10

    def resolve_collision(self, wall_rects):
        ### DEBUGGING ####
        # pygame.draw.rect(screen, (255, 0, 0), x_collision_hitbox, 2) # X-Axis hit-box display
        # pygame.draw.rect(screen, (0, 255, 0), y_collision_hitbox, 2) # Y-Axis hit-box display

        # Find the characters projected position for the next frame
        projected_x = self.x_position + self.x_velocity
        projected_y = self.y_position + self.y_velocity

        # Create hit-boxes for vertical and horizontal collisions
        x_collision_hitbox = pygame.Rect(projected_x + self.player_width_buffer , self.y_position, self.player_width - 2 * self.player_width_buffer, self.player_height)
        y_collision_hitbox = pygame.Rect(self.x_position + self.player_width // 2, projected_y, 2, self.player_height)

        for layer in wall_rects:
            for wall in layer:

                # X-Axis collision handling
                if wall.is_collidable and wall.platform_rect.colliderect(x_collision_hitbox):
                    # Right sided collision handling
                    if self.x_velocity > 0:
                        self.x_position = wall.platform_rect.left - self.player_width + self.player_width_buffer
                    # Left sided collision handling
                    elif self.x_velocity < 0:
                        self.x_position = wall.platform_rect.right - self.player_width_buffer

                # Y-Axis collision handling
                if wall.is_collidable and wall.platform_rect.colliderect(y_collision_hitbox):

                    # Landing collision handling
                    if self.y_velocity > 0:
                        # Reset Jump related attributes
                        self.is_touching_ground = True
                        self.jump_count = 0
                        self.jump_index = 0
                        # Set character y position
                        self.y_position = wall.platform_rect.top - self.player_height

                    # Hitting head collision handling
                    elif self.y_velocity <= 0:
                        self.y_velocity = 0
                        self.y_position = wall.platform_rect.bottom

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
