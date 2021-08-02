from Node import  Node
from Connection import Connection



class NeuralNetwork:
    def __init__(self, inputs_num, outputs_num):

        self.connections = []
        self.nodes = []
        self.nodes_ordered = []
        self.layers_cardinalities = [inputs_num, outputs_num]

        id_num = 0
        for i in range(inputs_num):
            self.nodes.append(Node(id_num, 0))
            id_num += 1

        for i in range(outputs_num):
            self.nodes.append(Node(id_num, 1))
            id_num += 1

        innov = 0
        for i in range(inputs_num):
            for j in range(outputs_num):
                connection = Connection(self.nodes[i],
                                        self.nodes[inputs_num+j],
                                        innov,
                                        True)
                self.connections.append(connection)
                innov += 1

        self.nodes_ordered = self.nodes.copy()
        self.nodes_ordered.sort(key=lambda x: x.layer)


    def is_fully_connected(self):
        connections_num = 0
        length = len(self.layers_cardinalities)
        for i in range(length-1):
            connections_num += self.layers_cardinalities[i] * sum(self.layers_cardinalities[i+1:length])

        if connections_num == len(self.connections):
            return True

        return False


