import numpy as np
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
from pole_balancing.PivotJoint import PivotJoint
from pole_balancing.Pole import Pole
from pole_balancing.progress_bar import printProgressBar
import sys


def init():
    space = pymunk.Space()
    space.gravity = 0, 30
    space.damping = 0.9

    floor = pymunk.Body(1, 100, pymunk.Body.STATIC)
    floor.position = 0, 590
    width, height = 600, 20
    floor_shape = pymunk.Poly(floor, [(0, 0), (width, 0), (width, height), (0, height)])
    floor_shape.elasticity = 0.7
    floor_shape.friction = 0.3
    space.add(floor, floor_shape)

    cart = pymunk.Body(1, 200, pymunk.Body.KINEMATIC)
    cart.position = 200, 490
    cart_shape = pymunk.Poly(cart, [(0, 0), (w, 0), (w, h), (0, h)])
    space.add(cart, cart_shape)

    p = Vec2d(450, 540)
    v = Vec2d(0, -250)
    p1 = Vec2d(250, 540)
    v1 = Vec2d(0, -100)
    poles = [Pole(space, p, v), Pole(space, p1, v1, color=(148, 78, 78, 0))]
    PivotJoint(space, cart_shape.body, poles[0].body, a=(250, 50))
    PivotJoint(space, cart_shape.body, poles[1].body, a=(50, 50))

    return space, poles, cart_shape


def check_game_over(angle, angle1, cart_pos, bound=pi / 6):
    if angle < -bound or angle > bound:
        return False, 0

    if angle1 < -bound or angle1 > bound:
        return False, 0

    if cart_pos < r or cart_pos + w > 600 - r:
        return False, 1

    return True, None


human_plays = False
visualise = True  # can't be False if human_plays is True
decision_frequency = 20  # how often will net be asked for decision(must be int > 0)
replay = True

wait_before_replay = False  # makes recording easier
blue = [0, 0, 255]
red = [255, 0, 0]
load_path = "dpb_champ_ver4.json"  # path from which the network for simulation is loaded
save_champ_path = "dpb_champ_ver4.json"  # path to which the overall champion will be saved

global running
global cart_speed

w, h = 300, 100  # cart parameters
r = 30  # border parameter


def main():
    passed_epochs = 0
    iterations = 0
    if replay:
        epochs = 1
        population = Population(1, config.INPUTS_NUM, config.OUTPUTS_NUM)
        population.organisms[0] = NeuralNetwork.load(load_path)
    elif human_plays:
        epochs = 1
        population = Population(1, config.INPUTS_NUM, config.OUTPUTS_NUM)
    else:
        epochs = config.EPOCHS
        population = Population(config.ORGANISMS_NUM, config.INPUTS_NUM, config.OUTPUTS_NUM)
        champion_fitness = []
        average_fitness = []
        std_fitness = []
        defeat_cause = [[0 for i in range(epochs)], [0 for i in range(epochs)]]
        printProgressBar(0, epochs, prefix='Progress:', suffix='Complete', length=50)

    for i in range(epochs):
        passed_epochs += 1
        observed_fitness = []
        if visualise:
            pygame.init()
            screen = pygame.display.set_mode((600, 600))
            clock = pygame.time.Clock()
            draw_options = pymunk.pygame_util.DrawOptions(screen)
            if wait_before_replay:
                time.sleep(10)

        for organism in population.organisms:
            global cart_speed
            cart_speed = -1
            global running
            running = True
            space, pole, cart = init()
            count = 1

            start = time.time()

            while running:
                if replay or human_plays:
                    iterations += 1

                if human_plays:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT:
                                cart_speed = -1
                            if event.key == pygame.K_RIGHT:
                                cart_speed = 1
                else:
                    if visualise:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                sys.exit()

                    count = count % decision_frequency

                    if count == 0:
                        inputs = [(cart.body.position[0] + w / 2 - 300) / (300 - w / 2 - r)]

                        for j in range(2):
                            inputs.append(pole[j].body.angular_velocity)
                            inputs.append(pole[j].body.angle * 6 / pi)

                        res = organism.feedforward(inputs)

                        if config.OUTPUTS_NUM == 2:
                            if res[0].output_val > res[1].output_val:
                                cart_speed = 1
                            else:
                                cart_speed = -1
                        else:
                            if config.TYPE == 0:
                                if res[0].output_val > config.DECISION_THRESHOLD:
                                    cart_speed = 1
                                else:
                                    cart_speed = -1
                            else:
                                cart_speed = res[0].output_val * 3

                        organism.fitness += 1
                        if organism.fitness > config.MIN_SOLUTION_FITNESS:
                            break

                    count += 1

                pos = cart.body.position
                running, cause = check_game_over(pole[0].body.angle, pole[1].body.angle, pos[0])

                if cause is not None and not human_plays and not replay:
                    defeat_cause[cause][i] += 1
                    if cause == 1:
                        organism.fitness -= config.OUT_OF_FIELD_PENALTY
                    else:
                        organism.fitness -= config.OUT_OF_ANGLE_PENALTY

                cart.body.position = (pos[0] + cart_speed, pos[1])

                if visualise:
                    screen.fill((127, 127, 127))
                    pygame.draw.line(screen, (0, 0, 0), (r, 0), (r, 600), width=3)
                    pygame.draw.line(screen, (0, 0, 0), (600 - r, 0), (600 - r, 600), width=3)
                    if cart_speed < 0:
                        color = blue
                    else:
                        color = red
                    pygame.draw.line(screen, color, (300 + 50 * cart_speed, 100), (300, 100), width=10)
                    space.debug_draw(draw_options)
                    pygame.display.update()
                    clock.tick(120)

                space.step(1 / 50)

            observed_fitness.append(organism.fitness)
            organism.fitness *= -1

        if replay or human_plays:
            end = time.time()
            print("Total time in seconds", end - start)
            print("Total iterations", iterations)

        if not human_plays and not replay:
            average_fitness.append(np.average(observed_fitness))
            std_fitness.append(np.std(observed_fitness))
            population.update_champion()
            champion_fitness.append(-population.champion.fitness)
            if population.champion.fitness < -config.MIN_SOLUTION_FITNESS:
                break

            population.create_species()

            population.natural_selection()

            population.create_next_generation()

            population.connections_history.clear()

            printProgressBar(i + 1, epochs, prefix='Progress:', suffix='Complete', length=50)

    if not human_plays and not replay:
        average_fitness = np.array(average_fitness)
        std_fitness = np.array(std_fitness)

        x = [i for i in range(passed_epochs)]
        plt.plot(x, champion_fitness, color='y', label='champ')

        plt.plot(x, average_fitness, color='b', label='avg')
        plt.fill_between(x, average_fitness - std_fitness,
                         average_fitness + std_fitness, color='b', alpha=0.2)

        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.title("Champion vs Average for pole balancing")
        plt.legend()
        plt.show()

        population.champion.save(save_champ_path)


if __name__ == "__main__":
    main()
