class Connection:
    def __init__(self, from_node, to_node, weight, innov=None):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
        self.innovation_number = innov
        self.enabled = True


