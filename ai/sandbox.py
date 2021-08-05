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

for node in a:
    node.layer += 1

print(a)
