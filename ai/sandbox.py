import copy

from Node import Node
from Connection import Connection
from NeuralNetwork import NeuralNetwork as nn
from random import uniform

net = nn(3, 2)

print(net.feedforward([0.5, 0, 1]))
# print(uniform(0, 1))
# print(net.is_fully_connected())

node = Node(0, 0)
node1 = Node(1, 0)
node2 = Node(2, 1)

a = [node, node1, node2]

print(a)

b = copy.deepcopy(a)

print(b)

a = [1, 2, 3, 4]
# a.insert(1, 4)
print(a[0:2])
print(a)
