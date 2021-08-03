from Node import Node
from Connection import Connection
from random import uniform


class NeuralNetwork:
    def __init__(self, inputs_num, outputs_num):

        self.connections = []
        self.nodes = []  # by id
        self.nodes_ordered = []  # by layers
        self.layers_cardinalities = [inputs_num, outputs_num]
        self.next_node_id = inputs_num + outputs_num

        id_num = 0
        for i in range(inputs_num):
            self.nodes.append(Node(id_num, 0))
            id_num += 1

        output_pos = 0
        for i in range(outputs_num):
            self.nodes.append(Node(id_num, 1, output_pos))
            id_num += 1
            output_pos += 1

        innov = 0
        for i in range(inputs_num):
            for j in range(outputs_num):
                connection = Connection(self.nodes[i],
                                        self.nodes[inputs_num + j],
                                        uniform(0, 1),
                                        innov)
                self.connections.append(connection)
                self.nodes[i].connections.append(connection)
                innov += 1

        self.nodes_ordered = self.nodes.copy()
        self.nodes_ordered.sort(key=lambda x: x.layer)

    def is_fully_connected(self):
        connections_num = 0
        length = len(self.layers_cardinalities)
        for i in range(length - 1):
            connections_num += self.layers_cardinalities[i] * sum(self.layers_cardinalities[i + 1:length])

        if connections_num == len(self.connections):
            return True

        return False


    def feedforward(self, inputs):
        for i in range(len(inputs)):
           self.nodes[i].output_val = inputs[i]

        res = []
        for node in self.nodes_ordered:
            if node.layer != 0:
                node.output_val = Node.sigmoid(node.output_sum)

            if node.layer == len(self.layers_cardinalities) - 1:
                res.append(node)
                continue

            for connection in node.connections:
                if connection.enabled:
                    connection.to_node.output_sum += connection.weight * node.output_val

        return res
