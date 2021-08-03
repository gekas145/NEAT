import numpy as np


class Node:
    def __init__(self, id_num, layer, output_pos=None):
        self.id = id_num
        self.layer = layer
        self.connections = []
        self.output_sum = 0.0
        self.output_val = 0.0
        self.output_pos = output_pos # None if not located in output layer

    def add_connection(self, connection):
        self.connections.append(connection)

    def __repr__(self):
        return "id: " + str(self.id) + ", layer: " + str(self.layer) + ", val: " + str(self.output_val)

    @staticmethod
    def sigmoid(x):
        return 1/(1 + np.exp(-x))
