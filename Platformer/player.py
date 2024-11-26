class Player:
    def __init__(self):
        self.screen_width, self.screen_height = 800, 600

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
        self.max_jumps = 2
        self.jump_count = 0
