import copy
import random
import numpy as np
from Node import Node
from Connection import Connection
from NeuralNetwork import NeuralNetwork as nn
from random import uniform, sample

from Population import Population

population = Population(2, 3, 2)

net = population.organisms[0]
net1 = population.organisms[1]

for i in range(2):
    population.add_node(net)

for i in range(2):
    population.add_connection(net)

net.draw()

net1.draw()

net2 = net.crossover(net1)

net2.draw()

