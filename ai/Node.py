class Node:
    def __init__(self, id_num, layer):
        self.id = id_num
        self.layer = layer
        self.connections = []

    def add_connection(self, connection):
        self.connections.append(connection)

    def __repr__(self):
        return str(self.layer)
