from neat.Population import Population
from pymunk import Vec2d
import pymunk
from pymunk.pygame_util import DrawOptions
import pygame
from math import pi


class Segment:
    # code for this class was taken from https://pymunk-tutorial.readthedocs.io/en/latest/joint/joint.html
    def __init__(self, space, p0, v, radius=10):
        self.body = pymunk.Body()
        self.body.position = p0
        shape = pymunk.Segment(self.body, (0, 0), v, radius)
        shape.density = 0.1
        shape.elasticity = 0.5
        shape.filter = pymunk.ShapeFilter(group=1)
        shape.color = (0, 255, 0, 0)
        space.add(self.body, shape)


class PivotJoint:
    # code for this class was partially taken from https://pymunk-tutorial.readthedocs.io/en/latest/joint/joint.html
    def __init__(self, space, b, b2, a=(0, 0), a2=(0, 0), collide=False):
        joint = pymunk.constraints.PinJoint(b, b2, a, a2)
        joint.collide_bodies = collide
        joint.distance = 0
        joint.error_bias = pow(0.001, 5)
        space.add(joint)


def init():
    space = pymunk.Space()
    space.gravity = 0, 50
    space.damping = 0.9

    floor = pymunk.Body(1, 100, pymunk.Body.STATIC)
    floor.position = 0, 590
    width, height = 600, 20
    floor_shape = pymunk.Poly(floor, [(0, 0), (width, 0), (width, height), (0, height)])
    floor_shape.elasticity = 0.7
    floor_shape.friction = 0.3
    space.add(floor, floor_shape)

    cart = pymunk.Body(1, 200, pymunk.Body.KINEMATIC)
    floor.position = 0, 590
    cart.position = 200, 490
    cart_shape = pymunk.Poly(cart, [(0, 0), (w, 0), (w, h), (0, h)])
    space.add(cart, cart_shape)

    p = Vec2d(350, 540)
    v = Vec2d(-50, -170)
    segment = Segment(space, p, v)
    PivotJoint(space, cart_shape.body, segment.body, a=(150, 50), collide=False)

    return space, segment, cart


def check_game_over(angle, cart_pos, bound=pi / 6):
    angle -= 0.27  # calculated empirically
    if angle < -bound or angle > bound:
        return False

    if cart_pos < 0 or cart_pos + w > 600:
        return False

    return True


human_plays = False
visualise = False  # can't be False if human_plays is True
decision_frequency = 20  # how often will net be asked for decision(must be int)

w, h = 300, 100  # cart parameters

# if visualise:
#     pygame.init()
#     screen = pygame.display.set_mode((600, 600))
#     clock = pygame.time.Clock()
#     draw_options = pymunk.pygame_util.DrawOptions(screen)


def main():
    if human_plays:
        epochs = 1
        population = Population(1, 3, 2)
    else:
        epochs = 300
        population = Population(150, 3, 2)
        champion_fitness = []

    for i in range(epochs):
        print("----------------------", "EPOCH:", i)
        if visualise:
            pygame.init()
            screen = pygame.display.set_mode((600, 600))
            clock = pygame.time.Clock()
            draw_options = pymunk.pygame_util.DrawOptions(screen)
        for organism in population.organisms:
            cart_speed = 0
            running = True
            space, segment, cart = init()
            count = 0
            while running:
                if human_plays:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT:
                                cart_speed = -1
                            if event.key == pygame.K_RIGHT:
                                cart_speed = 1
                else:
                    count = count % decision_frequency

                    if count == 0:
                        velocity = segment.body.angular_velocity
                        cart_pos = (cart.position[0] + w / 2 - 300) / (300 - w / 2)
                        angle = (segment.body.angle - 0.27) * 6 / pi

                        res = organism.feedforward([velocity, cart_pos, angle])

                        if res[0].output_val > res[1].output_val:
                            cart_speed = 1
                        else:
                            cart_speed = -1

                        organism.fitness += 1

                    count += 1

                pos = cart.position
                running = check_game_over(segment.body.angle, pos[0])
                cart.position = (pos[0] + cart_speed, pos[1])

                if visualise:
                    screen.fill((127, 127, 127))
                    space.debug_draw(draw_options)
                    pygame.display.update()
                    clock.tick(120)

                space.step(1 / 50)

            print(organism.fitness)
            organism.fitness *= -1

        if not human_plays:
            population.update_champion()
            champion_fitness.append(population.champion.fitness)

            population.create_species()
            # print(len(population.species))

            population.natural_selection()

            population.create_next_generation()

            population.connections_history.clear()

    if not human_plays:
        population.champion.save("champ.json")


if __name__ == "__main__":
    main()
