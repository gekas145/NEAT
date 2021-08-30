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


class Segment:
    def __init__(self, p0, v, radius=10):
        self.body = pymunk.Body()
        self.body.position = p0
        shape = pymunk.Segment(self.body, (0, 0), v, radius)
        shape.density = 0.1
        shape.elasticity = 0.5
        shape.filter = pymunk.ShapeFilter(group=1)
        shape.color = (0, 255, 0, 0)
        space.add(self.body, shape)


class PivotJoint:
    def __init__(self, b, b2, a=(0, 0), a2=(0, 0), collide=False):
        joint = pymunk.constraints.PinJoint(b, b2, a, a2)
        joint.collide_bodies = collide
        joint.distance = 0
        joint.error_bias = pow(0.001, 5)
        space.add(joint)


pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = 0, 30
space.damping = 0.9
draw_options = pymunk.pygame_util.DrawOptions(screen)


def create_body(x, y):
    body = pymunk.Body(10, 300, pymunk.Body.DYNAMIC)
    body.position = x, y
    # body.elasticity = 1
    shape = pymunk.Circle(body, 20)
    shape.density = 1
    shape.friction = 0.5
    shape.elasticity = 0.7
    space.add(body, shape)
    return shape


def draw_bodies(bodies):
    for body in bodies:
        x, y = int(body.body.position[0]), int(body.body.position[1])
        pygame.draw.circle(screen, (125, 0, 115), (x, y), 20)


def main():
    floor = pymunk.Body(1, 100, pymunk.Body.STATIC)
    floor.position = 0, 590
    width, height = 600, 20
    floor_shape = pymunk.Poly(floor, [(0, 0), (width, 0), (width, height), (0, height)])
    floor_shape.elasticity = 0.7
    floor_shape.friction = 0.3
    space.add(floor, floor_shape)

    cart = pymunk.Body(1, 200, pymunk.Body.KINEMATIC)
    w, h = 300, 100
    cart.position = 200, 490
    cart_shape = pymunk.Poly(cart, [(0, 0), (w, 0), (w, h), (0, h)])
    space.add(cart, cart_shape)

    b0 = space.static_body
    p = Vec2d(350, 540)
    v = Vec2d(-10, -170)
    segment = Segment(p, v)
    PivotJoint(cart_shape.body, segment.body, a=(150, 50), a2=(0, 0), collide=False)

    bodies = []
    # bodies.append(create_body(200, 200))

    running = True
    cart_speed = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                bodies.append(create_body(pos[0], pos[1]))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    cart_speed = -1
                    # cart.apply_force_at_local_point((400, 0), (h / 2, pos[1]))
                if event.key == pygame.K_RIGHT:
                    cart_speed = 1

        screen.fill((127, 127, 127))
        pos = cart.position
        cart.position = (pos[0] + cart_speed, pos[1])

        # pygame.draw.rect(screen, (0, 0, 0), [0, 590, width, height])
        # draw_bodies(bodies)
        space.debug_draw(draw_options)
        pygame.display.update()
        space.step(1 / 50)
        clock.tick(120)


if __name__ == "__main__":
    main()
