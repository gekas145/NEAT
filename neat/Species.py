import config as c
from random import uniform, sample


class Species:

    def __init__(self, organism):
        self.representative = organism.copy()
        self.organisms = [organism]
        self.average_fitness = 0.0
        self.previous_top_fitness = 0.0
        self.staleness = 0

    def fitness_sharing(self):
        for organism in self.organisms:
            organism.shared_fitness = organism.fitness / len(self.organisms)

    def calculate_average_fitness(self):
        self.fitness_sharing()
        self.average_fitness = 0.0
        for organism in self.organisms:
            self.average_fitness += organism.shared_fitness

        self.average_fitness /= len(self.organisms)

    def prepare(self):
        self.calculate_average_fitness()
        self.organisms.sort(key=lambda x: x.fitness)
        self.representative = self.organisms[0].copy()

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
