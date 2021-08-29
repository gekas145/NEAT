import copy
import random
import numpy as np
from pygame import QUIT, KEYDOWN, K_ESCAPE
from pymunk import Vec2d
import pymunk
from pymunk.pygame_util import DrawOptions

from Node import Node
from Connection import Connection
from NeuralNetwork import NeuralNetwork as nn
from random import uniform, sample

from Population import Population
import pygame

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = 0, 20

def create_body(x, y):
    body = pymunk.Body(10, 300, pymunk.Body.DYNAMIC)
    body.position = x, y
    body.elasticity = 100
    shape = pymunk.Circle(body, 20)
    space.add(body, shape)
    return shape

def draw_bodies(bodies):
    for body in bodies:
        x, y = int(body.body.position[0]), int(body.body.position[1])
        pygame.draw.circle(screen, (125, 0, 115), (x, y), 20)

def main():

    floor = pymunk.Body(1, 100, pymunk.Body.STATIC)
    floor.position = 10, 600
    floor.elasticity = 100
    w, h = 1000, 10
    vs = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
    shape = pymunk.Poly(floor, vs)
    space.add(floor, shape)

    bodies = []
    bodies.append(create_body(200, 200))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                bodies.append(create_body(pos[0], pos[1]))

        screen.fill((127, 127, 127))
        draw_bodies(bodies)
        pygame.display.update()
        space.step(1/50)
        clock.tick(120)

if __name__ == "__main__":
    main()
