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
population = Population(2, 3, 2)

net = population.organisms[0]
net1 = population.organisms[1]
#
# for i in range(5):
#     population.add_node(net)
# # print(net.is_fully_connected())
# #
# for node in net.nodes_ordered:
#     print(node)

# print(net.layers_cardinalities)
# # population.add_connection(net)
# # print(net.feedforward([0, 0.5, 1]))
# for connection in net.connections:
#     print("To:", connection.to_node, "|| From:", connection.from_node, "|| Enabled:", connection.enabled)
#
# print("===================net1=====================")

# population.add_node(net1)
# # print(net1.is_fully_connected())
# population.add_connection(net1)
#
# for node in net1.nodes:
#     print(node)
# print("--------------------")
# for con in net1.nodes[0].connections:
#     print(con.to_node)
# for i in range(3):
#     population.add_connection(net1)
# print(net1.is_fully_connected())

for i in range(3):
    population.add_node(net)

for i in range(3):
    population.add_connection(net)

net.draw()

