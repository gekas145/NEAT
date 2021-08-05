from NeuralNetwork import NeuralNetwork


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
                    connection.to_node.id == conn.from_node.id:
                return connection.innovation_number

        return None

    def add_connection(self):
        pass
