import pygame
import copy
from neat.Node import Node
from neat.Connection import Connection
from random import uniform, sample
from numpy.random import normal
import neat.config as c
import json


class NeuralNetwork:
    def __init__(self, inputs_num, outputs_num):

        self.connections = []  # sorted by innovation number
        self.bias_node = Node(0, 0)
        self.bias_node.output_val = 1
        self.nodes = [self.bias_node]  # sorted by id
        self.nodes_ordered = []  # sorted by layers
        self.layers_cardinalities = [inputs_num + 1, outputs_num]
        self.next_node_id = inputs_num + 1 + outputs_num
        self.input_nodes = [self.bias_node]
        self.output_nodes = []
        self.fitness = 0.0
        self.shared_fitness = 0.0

        id_num = 1
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
        for i in range(inputs_num + 1):
            for j in range(outputs_num):

                if self.nodes[i].id != 0:
                    weight = uniform(-1, 1)
                else:
                    weight = 0

                connection = Connection(self.nodes[i],
                                        self.nodes[inputs_num + 1 + j],
                                        weight,
                                        innov)
                self.connections.append(connection)
                self.nodes[i].connections.append(connection)
                innov += 1

        self.nodes_ordered = self.nodes.copy()
        self.prepare_nodes()

    def prepare_nodes(self):
        self.nodes_ordered.sort(key=lambda x: x.layer)

    def prepare_connections(self):
        # call to prepare for crossover
        self.connections.sort(key=lambda x: x.innovation_number)

    def copy(self):

        copied = NeuralNetwork(0, 0)
        copied.layers_cardinalities = self.layers_cardinalities.copy()

        for i in range(1, len(self.nodes)):
            node = self.nodes[i].copy()
            copied.nodes.append(node)

        for conn in self.connections:
            connection = Connection(copied.nodes[conn.from_node.id],
                                    copied.nodes[conn.to_node.id],
                                    conn.weight,
                                    conn.innovation_number)
            connection.enabled = conn.enabled
            copied.add_connection(connection)

        copied.next_node_id = self.next_node_id
        copied.bias_node = copied.nodes[0]
        copied.nodes_ordered = copied.nodes.copy()
        copied.prepare_nodes()

        for i in range(1, len(self.input_nodes)):
            copied.input_nodes.append(copied.nodes[self.input_nodes[i].id])

        for node in self.output_nodes:
            copied.output_nodes.append(copied.nodes[node.id])

        return copied

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
            self.input_nodes[i + 1].output_val = inputs[i]

        for node in self.nodes_ordered:
            if node.layer != 0:
                node.output_val = c.ACTIVATION_FUNCTION(node.output_sum)

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

        if node1.id == 0 or node2.id == 0:
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
                connection_right.weight = connection.weight
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

    def mutate_weight(self):
        connection = sample(self.connections, 1)[0]

        if uniform(0, 1) < c.RESET_WEIGHT_PROBABILITY:
            connection.weight = uniform(-1, 1)
        else:
            connection.weight += normal(0, 1) / 3
            # if connection.weight > 1:
            #     connection.weight = 1
            # elif connection.weight < -1:
            #     connection.weight = -1

    def crossover(self, net):
        # call on more fit parent
        self.prepare_connections()
        net.prepare_connections()

        child = NeuralNetwork(0, 0)
        child.layers_cardinalities = self.layers_cardinalities.copy()
        for i in range(1, len(self.nodes)):
            node = self.nodes[i].copy()
            child.nodes.append(node)

        this = copy.deepcopy(self.connections)
        that = copy.deepcopy(net.connections)

        this_conn = None
        that_conn = None

        while len(this) != 0 or this_conn is not None:
            if this_conn is None:
                this_conn = this.pop(0)

            if that_conn is None and len(that) != 0:
                that_conn = that.pop(0)

            if that_conn is None:
                connection = Connection(child.nodes[this_conn.from_node.id],
                                        child.nodes[this_conn.to_node.id],
                                        this_conn.weight,
                                        this_conn.innovation_number)

                if not this_conn.enabled:
                    if uniform(0, 1) < c.DISABLE_GENE_PROBABILITY:
                        connection.enabled = False

                child.add_connection(connection)

                this_conn = None
            elif this_conn.innovation_number > that_conn.innovation_number:
                that_conn = None
            elif this_conn.innovation_number == that_conn.innovation_number:
                if uniform(0, 1) < c.CHOOSE_ANOTHER_GENE_PROBABILITY:
                    conn = that_conn
                else:
                    conn = this_conn

                connection = Connection(child.nodes[conn.from_node.id],
                                        child.nodes[conn.to_node.id],
                                        conn.weight,
                                        conn.innovation_number)

                if not this_conn.enabled or not that_conn.enabled:
                    if uniform(0, 1) < c.DISABLE_GENE_PROBABILITY:
                        connection.enabled = False

                child.add_connection(connection)

                this_conn = None
                that_conn = None

            elif this_conn.innovation_number < that_conn.innovation_number:
                connection = Connection(child.nodes[this_conn.from_node.id],
                                        child.nodes[this_conn.to_node.id],
                                        this_conn.weight,
                                        this_conn.innovation_number)
                child.add_connection(connection)

                this_conn = None

        child.next_node_id = self.next_node_id
        child.bias_node = child.nodes[0]
        child.nodes_ordered = child.nodes.copy()
        child.prepare_nodes()

        for i in range(1, len(self.input_nodes)):
            child.input_nodes.append(child.nodes[self.input_nodes[i].id])

        for node in self.output_nodes:
            child.output_nodes.append(child.nodes[node.id])

        return child

    def get_difference(self, net):
        # returns measure of difference between `self` and `net` for speciation
        E = 0  # number of excess genes
        D = 0  # number of disjoint genes
        W = 0.0  # sum of weights diffs(to calculate the average diff)
        maximum = max(len(self.connections), len(net.connections))
        if maximum > c.MIN_GENOME_LENGTH:
            N = maximum  # length of bigger genome(1 if it's smaller than MIN_GENOME_LENGTH)
        else:
            N = 1
        joint_num = 0  # number of joint genes(to calculate the average diff)

        self.prepare_connections()
        net.prepare_connections()

        this = copy.deepcopy(self.connections)
        that = copy.deepcopy(net.connections)
        this_conn = this.pop(0)
        that_conn = that.pop(0)

        while this_conn is not None and that_conn is not None:

            if this_conn.innovation_number > that_conn.innovation_number:
                D += 1
                that_conn = None
            elif this_conn.innovation_number == that_conn.innovation_number:
                joint_num += 1
                W += abs(this_conn.weight - that_conn.weight)
                that_conn = None
                this_conn = None
            else:
                D += 1
                this_conn = None

            if this_conn is None and len(this) != 0:
                this_conn = this.pop(0)
            if that_conn is None and len(that) != 0:
                that_conn = that.pop(0)

        E += len(this) + len(that)

        if this_conn is not None or that_conn is not None:
            E += 1

        if joint_num != 0:
            W /= joint_num

        return c.EXCESS_GENE_COEFF * E / N + c.DISJOINT_GENE_COEFF * D / N + c.AVERAGE_WEIGHT_DIFF_COEFF * W

    def draw(self):
        (width, height) = (650, 650)
        white = (255, 255, 255)
        black = (0, 0, 0)
        blue = (0, 0, 255)
        red = (255, 0, 0)

        pygame.init()
        screen = pygame.display.set_mode((width, height))
        screen.fill(white)

        x = 50
        y = 30
        prev = 0
        prev_layer = 0
        circles = []
        for node in self.nodes_ordered:
            if node.layer > prev:
                prev = node.layer
                if self.layers_cardinalities[prev_layer] >= self.layers_cardinalities[prev_layer + 1]:
                    x += 70
                    y = 60
                else:
                    x += 70
                    y = 0
                prev_layer += 1
            y += 80
            pygame.draw.circle(screen, black, [x, y], 10)
            circles.append([x, y])

        for i in range(len(self.nodes_ordered)):
            for conn in self.nodes_ordered[i].connections:
                j = self.nodes_ordered.index(conn.to_node)
                if conn.enabled:
                    if conn.weight > 0:
                        color = red
                    elif conn.weight < 0:
                        color = blue
                    else:
                        color = black
                    pygame.draw.line(screen, color, circles[i], circles[j], round(abs(conn.weight) * 10 + 2))

        pygame.display.update()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    def __repr__(self):
        res = ''

        for connection in self.connections:
            res += 'From ' + str(connection.from_node.id) + ', '
            res += 'To ' + str(connection.to_node.id) + ', '
            res += 'Weight ' + str(connection.weight) + ', '
            res += 'Enabled ' + str(connection.enabled)
            res += '\n ------------------------------- \n'

        return res

    def save(self, filename):
        net_data = {"layers_cardinalities": self.layers_cardinalities.copy(),
                    "next_node_id": [self.next_node_id],
                    "fitness": [self.fitness]}

        nodes = []
        for node in self.nodes[1:len(self.nodes)]:
            nodes.append([node.id, node.layer])
        net_data["nodes"] = nodes

        connections = []
        for connection in self.connections:
            connections.append([connection.from_node.id,
                                connection.to_node.id,
                                connection.weight,
                                connection.innovation_number,
                                connection.enabled])
        net_data["connections"] = connections

        f = open(filename, "w")
        json.dump(net_data, f)
        f.close()

    @staticmethod
    def load(filename):
        f = open(filename, "r")
        net_data = json.load(f)
        f.close()

        net = NeuralNetwork(0, 0)

        net.layers_cardinalities = net_data["layers_cardinalities"].copy()
        net.fitness = net_data["fitness"][0]

        last_layer_num = len(net.layers_cardinalities) - 1
        for node in net_data["nodes"]:
            nd = Node(node[0], node[1])
            net.nodes.append(nd)
            if node[1] == 0:
                net.input_nodes.append(nd)
            elif node[1] == last_layer_num:
                net.output_nodes.append(nd)

        for conn in net_data["connections"]:
            connection = Connection(net.nodes[int(conn[0])],
                                    net.nodes[int(conn[1])],
                                    conn[2],
                                    int(conn[3]))
            connection.enabled = conn[4]
            net.add_connection(connection)

        net.next_node_id = net_data["next_node_id"][0]

        net.nodes_ordered = net.nodes.copy()
        net.prepare_nodes()

        return net

