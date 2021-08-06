from Node import Node
from Connection import Connection
from random import uniform


class NeuralNetwork:
    def __init__(self, inputs_num, outputs_num):

        self.connections = []  # sorted by innovation number
        self.nodes = []  # sorted by id
        self.nodes_ordered = []  # sorted by layers
        self.layers_cardinalities = [inputs_num, outputs_num]
        self.next_node_id = inputs_num + outputs_num
        self.input_nodes = []
        self.output_nodes = []

        id_num = 0
        for i in range(inputs_num):
            node = Node(id_num, 0)
            self.nodes.append(node)
            self.input_nodes.append(node)
            id_num += 1

        for i in range(outputs_num):
            node = Node(id_num, 1)
            self.nodes.append(node)
            self.output_nodes.append(node)
            id_num += 1

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
        self.prepare_nodes()

    def prepare_nodes(self):
        self.nodes_ordered.sort(key=lambda x: x.layer)

    def prepare_connections(self):
        self.connections.sort(key=lambda x: x.innovation_number)

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
            self.input_nodes[i].output_val = inputs[i]

        for node in self.nodes_ordered:
            if node.layer != 0:
                node.output_val = Node.sigmoid(node.output_sum)

            if node.layer == len(self.layers_cardinalities) - 1:
                node.output_sum = 0
                continue

            for connection in node.connections:
                if connection.enabled:
                    connection.to_node.output_sum += connection.weight * node.output_val

            node.output_sum = 0

        return self.output_nodes

    def check_nodes(self, node1, node2, criterion):
        # criterion - bool, True if used before add_node, False if before add_connection
        if node1.layer == node2.layer:
            return False

        for connection in self.connections:
            if connection.from_node.id == node1.id and connection.to_node.id == node2.id:
                return criterion
            if connection.from_node.id == node2.id and connection.to_node.id == node1.id:
                return criterion

        return not criterion

    def add_connection(self, connection):
        self.nodes[connection.from_node.id].add_connection(connection)
        self.connections.append(connection)

    def add_node(self, connection_left, connection_right):
        for connection in self.connections:
            if connection.from_node.id == connection_left.from_node.id and \
                    connection.to_node.id == connection_right.to_node.id:
                connection.enabled = False
                break

        node = connection_left.to_node
        layer = connection_left.to_node.layer
        self.nodes.append(node)
        self.add_connection(connection_left)
        self.add_connection(connection_right)

        if connection_right.to_node.layer - connection_left.from_node.layer == 1:
            self.layers_cardinalities.insert(layer, 1)
            start = sum(self.layers_cardinalities[0:layer])
            for i in range(start, len(self.nodes_ordered)):
                self.nodes_ordered[i].layer += 1
        else:
            self.layers_cardinalities[layer] += 1

        self.nodes_ordered.append(node)
        self.prepare_nodes()
