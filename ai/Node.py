import numpy as np


class Node:
    def __init__(self, id_num, layer):
        self.id = id_num
        self.layer = layer
        self.connections = []
        self.output_sum = 0.0
        self.output_val = 0.0

    def add_connection(self, connection):
        self.connections.append(connection)

    def __repr__(self):
        return "id: " + str(self.id) + ", layer: " + str(self.layer) + ", val: " + str(self.output_val)

    def copy(self):
        return Node(self.id, self.layer)

    @staticmethod
    def sigmoid(x):
        return 1/(1 + np.exp(-x))
