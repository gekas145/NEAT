import pygame
import copy
from Node import Node
from Connection import Connection
from random import uniform, sample
from numpy.random import normal
import config as c


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
        for i in range(inputs_num+1):
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
        connection.weight += normal(0, 1)

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

        for node in self.input_nodes:
            child.input_nodes.append(child.nodes[node.id])

        for node in self.output_nodes:
            child.output_nodes.append(child.nodes[node.id])

        return child

    def difference(self, net):
        # returns measure of difference between `self` and `net` for speciation
        pass

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

