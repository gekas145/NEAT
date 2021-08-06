from NeuralNetwork import NeuralNetwork
from random import sample, uniform, randint
from Connection import Connection
from Node import Node


class Population:
    def __init__(self, n, inputs_num, outputs_num):
        self.connections_history = []
        self.organisms = []
        self.next_innovation_num = inputs_num * outputs_num
        self.species = []

        for i in range(n):
            self.organisms.append(NeuralNetwork(inputs_num, outputs_num))

    def check_innovation_num(self, conn):
        for connection in self.connections_history:
            if connection.from_node.id == conn.from_node.id and \
                    connection.to_node.id == conn.to_node.id:
                return connection.innovation_number

        return None

    def check_connection(self, connection):
        innov = self.check_innovation_num(connection)
        if innov is not None:
            connection.innovation_number = innov
        else:
            connection.innovation_number = self.next_innovation_num
            self.next_innovation_num += 1
            self.connections_history.append(connection)

    def add_connection(self, net):
        if net.is_fully_connected():
            print("failed")
            return

        node1, node2 = sample(net.nodes, 2)
        while not net.check_nodes(node1, node2, False):
            node1, node2 = sample(net.nodes, 2)

        if node1.layer > node2.layer:
            node1, node2 = node2, node1

        connection = Connection(node1, node2, uniform(0, 1))
        self.check_connection(connection)
        net.add_connection(connection)

    def add_node(self, net):
        node1, node2 = sample(net.nodes, 2)
        while not net.check_nodes(node1, node2, True):
            node1, node2 = sample(net.nodes, 2)

        if node1.layer > node2.layer:
            node1, node2 = node2, node1

        if node2.layer - node1.layer == 1:
            node = Node(net.next_node_id, node2.layer)
        else:
            node = Node(net.next_node_id, randint(node1.layer + 1, node2.layer - 1))
        net.next_node_id += 1

        connection1 = Connection(node1, node, uniform(0, 1))
        self.check_connection(connection1)

        connection2 = Connection(node, node2, uniform(0, 1))
        self.check_connection(connection2)

        net.add_node(connection1, connection2)
