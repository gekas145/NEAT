from NeuralNetwork import NeuralNetwork
from random import sample, uniform, randint
from Connection import Connection
from Node import Node
from Species import Species
import config as c


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

    def prepare_species(self):
        for species in self.species:
            species.organisms.sort(key=lambda x: x.fitness)

        self.species.sort(key=lambda x: x.shared_fitness)

    def add_connection(self, net):
        if net.is_fully_connected():
            print("failed")
            return

        node1, node2 = sample(net.nodes, 2)
        while not net.check_nodes(node1, node2, False):
            node1, node2 = sample(net.nodes, 2)

        if node1.layer > node2.layer:
            node1, node2 = node2, node1

        connection = Connection(node1, node2, uniform(-1, 1))
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

        connection1 = Connection(node1, node, 1)
        self.check_connection(connection1)

        connection2 = Connection(node, node2, None)  # will be later changed to weight between node1 and node2
        self.check_connection(connection2)

        net.add_node(connection1, connection2)

        connection3 = Connection(net.bias_node, node, 0)
        self.check_connection(connection3)

        net.add_connection(connection3)

    def create_species(self):
        for organism in self.organisms:
            added = False
            for species in self.species:
                if species.representative.get_difference(organism) < c.COMPATIBILITY_THRESHOLD:
                    species.organisms.append(organism)
                    added = True
                    break

            if not added:
                self.species.append(Species(organism))

        for species in self.species:
            species.calculate_shared_fitness()

    def natural_selection(self):
        pass

    def get_offspring(self):
        pass

    def create_next_generation(self):
        pass
