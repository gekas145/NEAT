import copy
import random
import numpy as np
from Node import Node
from Connection import Connection
from NeuralNetwork import NeuralNetwork as nn
from random import uniform, sample

from ai.Population import Population

# net = nn(3, 2)
node = Node(0, 0)
node1 = Node(1, 0)
node2 = Node(2, 1)
population = Population(1, 3, 2)

net = population.organisms[0]

# for i in range(5):
#     population.add_node(net)
# # print(net.feedforward([0.5, 1, 1]))
#
# for node in net.nodes_ordered:
#     print(node)
# population.add_connection(net)
# print(net.feedforward([0, 0.5, 1]))

print(net.connections[0])
print(net.connections[0].weight)
net.mutate_weight()
print(net.connections[0])
print(net.connections[0].weight)
