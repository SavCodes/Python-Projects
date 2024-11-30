import pygame
import paddle
import ball

# TO DO LIST:
# - Add round timer and total game timer
# - Add dynamic bouncing to paddles based on movement or collision location

# Check if the game was quit
def event_checker():
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True

def initialize_game():
    pygame.init()
    game_icon = pygame.image.load("pong_icon.png")
    pygame.display.set_icon(game_icon)
    pygame.display.set_caption("Pong", "Pong")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    return screen, clock

# Run the main game loop
def main():
    # Create required pygame objects
    screen, clock = initialize_game()

    # Create the ball
    game_ball = ball.Ball(screen)

    # Create player paddles
    player_one = paddle.Paddle(screen.get_width() * 0.05 , screen.get_height() / 2, arrow_key_controls=False)
    player_two = paddle.Paddle(screen.get_width() * 0.95, screen.get_height() / 2)

    running = True
    while running:
        screen.fill((0, 0, 0))                              # Reset screen between frames
        running = event_checker()                           # Check if game was quit
        player_one.render_paddle(screen)                    # Draw player one's paddle to screen
        player_two.render_paddle(screen)                    # Draw player two's paddle to screen

        game_ball.check_collisions(player_one, player_two)  # Check if the ball made contact with paddles
        game_ball.render_ball()                             # Display the ball
        game_ball.render_score()                            # Display the score

        pygame.display.flip()                               # Update the screen after drawing all objects
        clock.tick(60)                                      # Cap FPS at 60

    pygame.quit()

if __name__ == '__main__':
    main()
