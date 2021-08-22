from NeuralNetwork import NeuralNetwork
from random import sample, uniform, randint, choices
from Connection import Connection
from Node import Node
from Species import Species
import config as c
from math import floor
import numpy as np



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
            species.calculate_average_fitness()

        self.species.sort(key=lambda x: x.average_fitness)

    def erase_species(self):
        for species in self.species:
            species.organisms.clear()

    def add_connection(self, net):
        if net.is_fully_connected():
            # print("failed")
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

                    if organism.fitness > species.representative.fitness:
                        species.representative = organism.copy()

                    break

            if not added:
                self.species.append(Species(organism))

    def natural_selection(self):
        to_delete = []

        for i in range(len(self.species)):

            if len(self.species[i].organisms) == 0:
                to_delete.append(i)
                continue
            else:
                self.species[i].prepare()

            if self.species[i].representative.fitness > self.species[i].previous_top_fitness:
                self.species[i].previous_top_fitness = self.species[i].representative.fitness
                self.species[i].staleness = 0
            else:
                self.species[i].staleness += 1

            if self.species[i].staleness == c.MAX_STALENESS:
                to_delete.append(i)
            else:  # delete the bottom half
                self.species[i].organisms = self.species[i].organisms[0:len(self.species[i].organisms) // 2 + 1]
                self.species[i].calculate_average_fitness()

        for i in range(len(to_delete) - 1, -1, -1):
            self.species.pop(to_delete[i])
            # if i < len(to_delete) - 1:
            #     to_delete[i+1:len(to_delete)] -= 1

        self.prepare_species()

    def add_offspring(self, species):
        if uniform(0, 1) < c.CROSSOVER_PROBABILITY:

            parent1, parent2 = choices(species.organisms, k=2)

            if parent2.fitness > parent1.fitness:
                parent1, parent2 = parent2, parent1

            child = parent1.crossover(parent2)

        else:
            child = sample(species.organisms, 1)[0].copy()

        if uniform(0, 1) < c.ADD_CONNECTION_PROBABILITY:
            self.add_connection(child)
        if uniform(0, 1) < c.ADD_NODE_PROBABILITY:
            self.add_node(child)
        if uniform(0, 1) < c.MUTATE_WEIGHT_PROBABILITY:
            child.mutate_weight()

        self.organisms.append(child)

    def create_next_generation(self):
        n = len(self.organisms)

        self.organisms.clear()

        average_sum = 0.0
        for species in self.species:
            average_sum += species.average_fitness
            self.organisms.append(species.organisms[0])  # add best of each species without mutations

        for species in self.species:
            children_num = floor(species.average_fitness/average_sum * n) - 1

            for i in range(children_num):
                self.add_offspring(species)

        while len(self.organisms) < n:
            self.add_offspring(self.species[0])

        self.erase_species()

