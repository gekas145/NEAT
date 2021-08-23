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

        # print(len(self.organisms))
        self.average_fitness /= len(self.organisms)

    def prepare(self):
        # self.calculate_average_fitness()
        self.organisms.sort(key=lambda x: x.fitness)
        self.representative = self.organisms[0].copy()

