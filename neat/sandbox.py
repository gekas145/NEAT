# File for quick tests
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

net = Population(1, 5, 1).organisms[0]

net1 = nn.load("C:/Users/yevhe/PycharmProjects/NEAT/double_pole_balancing/dpb_champ_ver4.json")
# net1 = nn.load("C:/Users/yevhe/PycharmProjects/NEAT/pole_balancing/champ_ver3.json")
net1.draw()
print(net1)
print(net1.fitness)
print(net.get_difference(net1))