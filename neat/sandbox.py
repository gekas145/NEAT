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

population = Population(1, 2, 2)
net = population.organisms[0]

population.add_node(net)
population.add_node(net)

# net.draw()
# print(net.feedforward([0.5, 0.72]))

# net.save("test.json")
# print(net.feedforward([0.5, 0.72]))

net1 = nn.load("xor_champ.json")
# net1.draw()
print(net1.feedforward([0, 1]))
