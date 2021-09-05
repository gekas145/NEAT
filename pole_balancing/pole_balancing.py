import numpy as np
import sys
from neat.Population import Population
from pymunk import Vec2d
import pymunk
from pymunk.pygame_util import DrawOptions
import pygame
from math import pi
from matplotlib import pyplot as plt
from neat.NeuralNetwork import NeuralNetwork
import time
import neat.config as config


# Print iterations progress
# this code was taken from
# https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console?page=1&tab=votes#tab-top
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    # Print New Line on Complete
    if iteration == total:
        print()

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
        return False, 0

    if cart_pos < r or cart_pos + w > 600 - r:
        return False, 1

    return True, None


human_plays = False
visualise = True  # can't be False if human_plays is True
decision_frequency = 20  # how often will net be asked for decision(must be int)
replay = True

w, h = 300, 100  # cart parameters
r = 60  # border parameter


def main():
    if replay:
        epochs = 1
        population = Population(1, 3, 2)
        population.organisms[0] = NeuralNetwork.load("champ_ver2.json")
    elif human_plays:
        epochs = 1
        population = Population(1, 3, 2)
    else:
        epochs = 200
        population = Population(150, 3, 2)
        champion_fitness = []
        average_fitness = []
        std_fitness = []
        defeat_cause = [[0 for i in range(epochs)], [0 for i in range(epochs)]]
        printProgressBar(0, epochs, prefix='Progress:', suffix='Complete', length=50)

    for i in range(epochs):
        observed_fitness = []
        # sys.stdout.write("\r---------------------- EPOCH:" + str(i))
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

            start = time.time()

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
                        cart_pos = (cart.position[0] + w / 2 - 300) / (300 - w / 2 - r)
                        angle = (segment.body.angle - 0.27) * 6 / pi

                        res = organism.feedforward([velocity, cart_pos, angle])

                        if res[0].output_val > res[1].output_val:
                            cart_speed = 1
                        else:
                            cart_speed = -1
                        # print(cart_speed)

                        if abs(cart_pos) < config.CENTER_ACCEPTABLE_DEVIATION:
                            organism.fitness += config.CENTER_REWARD
                        else:
                            organism.fitness += config.USUAL_REWARD

                    count += 1

                pos = cart.position
                running, cause = check_game_over(segment.body.angle, pos[0])

                if cause is not None and not human_plays and not replay:
                    defeat_cause[cause][i] += 1
                    if cause == 1:
                        organism.fitness -= config.OUT_OF_FIELD_PENALTY
                    else:
                        organism.fitness -= config.OUT_OF_ANGLE_PENALTY

                cart.position = (pos[0] + cart_speed, pos[1])

                if visualise:
                    screen.fill((127, 127, 127))
                    pygame.draw.line(screen, (0, 0, 0), (r, 0), (r, 600), width=3)
                    pygame.draw.line(screen, (0, 0, 0), (600 - r, 0), (600 - r, 600), width=3)
                    space.debug_draw(draw_options)
                    pygame.display.update()
                    clock.tick(120)

                space.step(1 / 50)

            # print(organism.fitness)
            observed_fitness.append(organism.fitness)
            organism.fitness *= -1

        if replay:
            end = time.time()
            print(end - start)

        if not human_plays and not replay:
            average_fitness.append(np.average(observed_fitness))
            std_fitness.append(np.std(observed_fitness))
            population.update_champion()
            champion_fitness.append(-population.champion.fitness)

            population.create_species()
            # print(len(population.species))

            population.natural_selection()

            population.create_next_generation()

            population.connections_history.clear()

            printProgressBar(i + 1, epochs, prefix='Progress:', suffix='Complete', length=50)

    if not human_plays and not replay:
        average_fitness = np.array(average_fitness)
        std_fitness = np.array(std_fitness)

        x = [i for i in range(epochs)]
        plt.plot(x, champion_fitness, color='y', label='champ')

        plt.plot(x, average_fitness, color='b', label='avg')
        plt.fill_between(x, average_fitness - std_fitness,
                         average_fitness + std_fitness, color='b', alpha=0.2)

        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.title("Champion vs Average for pole balancing")
        plt.legend()
        plt.show()

        plt.title("Defeat causes in pole balancing")
        plt.xlabel("Generation")
        plt.ylabel("Number")
        plt.plot(x, defeat_cause[0], color='y', label='angle out')
        plt.plot(x, defeat_cause[1], color='b', label='field out')
        plt.legend()
        plt.show()

        population.champion.save("champ_ver2.json")


if __name__ == "__main__":
    main()
