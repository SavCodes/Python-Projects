import pygame
import sliders

#Zeroth Order Oscillator
#   Newtowns force law: F = m * a
#   Hookes law spring force: F = -k * x
#   Deriving for acceleration: a = (-k * x) / m

#First Order Oscillator
#   Newtowns force law: F = m * a
#   Hookes law spring force: F = -k * x  -c * v + F_external
#   Deriving for acceleration: (-k * x  -c * v + F_external) / m



class WaterNode:
    def __init__(self, x, y, m):
        # PHYSICS RELATED LOAD UPS
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0.0, 0.0)
        self.acceleration = pygame.math.Vector2(0.0, 0.0)

        self.equilibrium_position = pygame.math.Vector2(x, y)
        self.displacement_distance = self.position[1] - self.equilibrium_position[1]

        self.m = m
        self.k = 0.5
        self.c = 0.2

    def display(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.m)

    #   Deriving for acceleration: (-k * x  -c * v + F_external) / m
    def zeroth_order_oscillation_update_physics(self):
        self.displacement_distance =  self.equilibrium_position - self.position
        self.acceleration = (self.k * self.displacement_distance) / self.m
        self.velocity += self.acceleration
        self.position += self.velocity



    #   Deriving for acceleration: (-k * x  -c * v + F_external) / m
    def first_order_oscillation_update_physics(self):
        self.displacement_distance =  self.equilibrium_position - self.position
        self.acceleration = (self.k * self.displacement_distance - self.c * self.velocity) / self.m
        self.velocity += self.acceleration
        self.position += self.velocity

        if self.velocity.magnitude() < 0.1:
            self.velocity = pygame.math.Vector2(0.0, 0.0)

    def displace_node(self, vertical_displacement_distance):
        self.position[1] += vertical_displacement_distance

def create_water_node_list(list_length):
    return [WaterNode(100+i*(500/list_length), 200, 10) for i in range(list_length)]



def event_checker():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True

def main():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    water_nodes = create_water_node_list(100)
    clock = pygame.time.Clock()

    water_nodes[len(water_nodes)//2].displace_node(25)
    slider,output = sliders.initialize_slider(screen)

    running = True
    while running:
        dampener = 0.01
        running = event_checker()
        for node_index, node in enumerate(water_nodes):

            if node_index > 0:
                left_delta = node.position[1] - water_nodes[node_index - 1].position[1]
                water_nodes[node_index - 1].velocity[1] += left_delta * dampener

            if node_index < len(water_nodes) - 1:
                right_delta = node.position[1] - water_nodes[node_index + 1].position[1]
                water_nodes[node_index + 1].velocity[1] += right_delta * dampener


            node.display(screen)
            node.first_order_oscillation_update_physics()


        sliders.draw_slider(slider, output)
        pygame.display.update()
        clock.tick(60)
        screen.fill((0,0,0))
    pygame.quit()

if __name__ == '__main__':
    main()

