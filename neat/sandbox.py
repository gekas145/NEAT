import copy
import random
import numpy as np
from Node import Node
from Connection import Connection
from NeuralNetwork import NeuralNetwork as nn
from random import uniform, sample

from Population import Population



net = nn(0, 0)

for i in range(1, 5):
    net.nodes.append(Node(i, 0))

net.nodes[3].layer = 2
net.nodes[4].layer = 1

net.input_nodes.append(net.nodes[1])
net.input_nodes.append(net.nodes[2])
net.output_nodes.append(net.nodes[3])

net.layers_cardinalities = [3, 1, 1]

net.add_connection(Connection(net.nodes[0], net.nodes[3], 1))
net.add_connection(Connection(net.nodes[0], net.nodes[4], -0.96412))
net.add_connection(Connection(net.nodes[2], net.nodes[3], 0.32547))
net.add_connection(Connection(net.nodes[1], net.nodes[4], 1))
net.add_connection(Connection(net.nodes[4], net.nodes[3], -0.71137))
connection = Connection(net.nodes[1], net.nodes[3], 0.90078)
connection.enabled = False
net.add_connection(connection)

net.nodes_ordered = net.nodes.copy()
net.prepare_nodes()

net1 = net.copy()

# net1.draw()

print(net1.feedforward([0, 0])[0].output_val - net.feedforward([0, 0])[0].output_val)
print(net1.feedforward([1, 1])[0].output_val - net.feedforward([1, 1])[0].output_val)
print(net1.feedforward([0, 1])[0].output_val - net.feedforward([0, 1])[0].output_val)
print(net1.feedforward([1, 0])[0].output_val - net.feedforward([1, 0])[0].output_val)
print(net.input_nodes)
# for node in net1.nodes_ordered:
#     print("------------------------")
#     print("From", node.id)
#     for conn in node.connections:
#         print("To", conn.to_node.id, conn.weight, conn.enabled)
print(net1.input_nodes)



