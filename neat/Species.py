class Species:

    def __init__(self, representative):
        self.representative = representative
        self.organisms = [representative]
        self.shared_fitness = 0.0
        self.top_fitness_representative = representative
        self.previous_shared_fitness = 0.0
        self.stainless = 0

    def calculate_shared_fitness(self):
        for organism in self.organisms:
            self.shared_fitness += organism.fitness

        self.shared_fitness /= len(self.organisms)

