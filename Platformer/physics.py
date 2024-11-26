def gravity(sprite, gravity_value=0.5):
    if not sprite.is_touching_ground:
        sprite.y_acceleration = gravity_value
    else:
        sprite.y_acceleration = 0
        sprite.y_velocity = 0


def update_physics(sprite):
    # Update the position based on velocity
    sprite.x_position += sprite.x_velocity
    sprite.y_position += sprite.y_velocity

    # Update the velocity based on acceleration
    sprite.x_velocity += sprite.x_acceleration
    sprite.y_velocity += sprite.y_acceleration
