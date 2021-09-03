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

population = Population(2, 2, 2)
net = population.organisms[0]
net2 = population.organisms[1]

population.add_node(net)
population.add_node(net)
population.add_node(net2)
# net.draw()
# print(net.feedforward([0.5, 0.72]))

# net.save("test.json")
# print(net.feedforward([0.5, 0.72]))

net1 = nn.load("xor_champ.json")
net1.draw()
for a in range(2):
    for b in range(2):
        print([a, b], net1.feedforward([a, b]))

print(net1.fitness)
# for connection in population.connections_history:
#     print("From", connection.from_node.id, "To", connection.to_node.id, "Innov", connection.innovation_number)