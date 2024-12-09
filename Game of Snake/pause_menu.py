import pygame
import math

class PauseMenu:
    def __init__(self, screen, gamestates):
        self.screen = screen
        self.bob_index = 0
        self.width, self.height = pygame.display.get_window_size()
        self.is_music_paused = False
        self.pause_gamestates = self.create_pause_gamestates(gamestates)

    def create_pause_gamestates(self, gamestates):
        index_y_start, index_x_start = len(gamestates) // 4, len(gamestates[0]) // 4
        index_y_end, index_x_end = 2 * len(gamestates) // 4, 2 * len(gamestates[0]) // 4
        pause_gamestates = [row[index_x_start:index_x_end] for row in gamestates[index_y_start:index_y_end]]
        return pause_gamestates

    def display_pause_title(self):
        # Displays "Game Paused!" Start --------------------------------------------
        pause_text = "Game Paused!"
        pause_size = self.width // 8
        my_font = pygame.font.SysFont('Comic Sans MS', pause_size)
        pause_surface = my_font.render(pause_text, True, "black")
        pause_rect = pause_surface.get_rect(center=(self.width // 2, self.height // 2 + 20* math.sin(self.bob_index / 100)))
        self.screen.blit(pause_surface, pause_rect)

        # Display "Game Pause!" End ------------------------------------------------

        # Title Bobbing Logic Start ------------------------------------------------
        if self.bob_index < math.pi * 100:
            self.bob_index += 1
        else:
            self.bob_index = 0
        # Title Bobbing Logic End --------------------------------------------------

    def display_pause_instructions(self):
        # Displays Pause Instructions Start ----------------------------------------
        instructions_text = "Press Space to Pause/Unpause"
        instructions_size = self.width // 20
        my_font = pygame.font.SysFont('Comic Sans MS', instructions_size)
        instruction_surface = my_font.render(instructions_text, True, "white")
        instruction_rect = instruction_surface.get_rect(center=(self.width * 0.5, self.height * 0.7))
        self.screen.blit(instruction_surface, instruction_rect)
        # Display Pause Instructions End -------------------------------------------

    def display_move_instructions(self):
        # Displays Move Instructions Start -----------------------------------------
        move_instructions_text = "Use the arrow keys or w, a, s, d to move"
        move_instructions_size = self.width // 20
        my_font = pygame.font.SysFont('Comic Sans MS', move_instructions_size)
        move_instruction_surface = my_font.render(move_instructions_text, True, "black")
        move_instruction_rect = move_instruction_surface.get_rect(center=(self.width // 2, self.height * 0.77))
        self.screen.blit(move_instruction_surface, move_instruction_rect)
        # Display Move Instructions End --------------------------------------------

    def display_mute_instructions(self):
        # Displays Mute Instructions Start -----------------------------------------
        mute_instructions_text = "Press 'm' to Mute/Unmute Sound"
        mute_instructions_size = self.width // 20
        my_font = pygame.font.SysFont('Comic Sans MS', mute_instructions_size)
        mute_instruction_surface = my_font.render(mute_instructions_text, True, "black")
        mute_instruction_rect = mute_instruction_surface.get_rect(center=(self.width // 2, self.height * 0.84))
        self.screen.blit(mute_instruction_surface, mute_instruction_rect)
        # Display Mute Instructions End --------------------------------------------

    def run_pause_menu(self):
        self.display_pause_title()
        self.display_pause_instructions()
        self.display_move_instructions()
        self.display_mute_instructions()
        pygame.display.update()
