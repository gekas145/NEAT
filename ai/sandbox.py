from Node import Node
from Connection import Connection
from NeuralNetwork import NeuralNetwork as nn
from random import uniform

net = nn(3, 2)

print(net.feedforward([0.5, 0, 1]))
print(uniform(0, 1))


