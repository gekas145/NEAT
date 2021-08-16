import config as c
from random import uniform, sample


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

    def get_offspring(self):
        if uniform(0, 1) < c.CROSSOVER_PROBABILITY:

            parent1, parent2 = sample(self.organisms, 2)
            if parent2.fitness > parent1.fitness:
                parent1, parent2 = parent2, parent1

            child = parent1.crossover(parent2)

        else:
            pass
