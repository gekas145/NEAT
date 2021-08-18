import config as c
from random import uniform, sample


class Species:

    def __init__(self, organism):
        self.representative = organism.copy()
        self.organisms = [organism]
        self.shared_fitness = 0.0
        self.top_fitness_representative = organism.copy()
        self.previous_top_fitness = 0.0
        self.staleness = 0

    def prepare(self):
        self.previous_top_fitness = self.top_fitness_representative.fitness
        for organism in self.organisms:
            self.shared_fitness += organism.fitness
            if organism.fitness > self.top_fitness_representative.fitness:
                self.top_fitness_representative = organism.copy()

        self.shared_fitness /= len(self.organisms)

    def get_offspring(self, population):
        if uniform(0, 1) < c.CROSSOVER_PROBABILITY:

            parent1, parent2 = sample(self.organisms, 2)
            if parent2.fitness > parent1.fitness:
                parent1, parent2 = parent2, parent1

            child = parent1.crossover(parent2)

        else:
            child = sample(self.organisms, 1)[0].copy()

        if uniform(0, 1) < c.ADD_CONNECTION_PROBABILITY:
            population.add_connection(child)
        if uniform(0, 1) < c.ADD_NODE_PROBABILITY:
            population.add_node(child)
        if uniform(0, 1) < c.MUTATE_WEIGHT_PROBABILITY:
            child.mutate_weight()

        population.organisms.append(child)
