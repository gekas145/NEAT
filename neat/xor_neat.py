import math

from Population import Population
from numpy.random import binomial as bin
from random import uniform
from math import floor


def xor(x, y):
    return (x + y) % 2


def log_and(x, y):
    if x == 0 or y == 0:
        return 0
    return 1


def evaluate_log_and(organism):
    for a in range(2):
        for b in range(2):
            output_val = organism.feedforward([a, b])[0].output_val
            if a == 0 or b == 0:
                organism.fitness += abs(output_val - log_and(a, b))
            else:
                organism.fitness += abs(output_val - log_and(a, b)) * 2


def evaluate_xor(organism):
    for a in range(2):
        for b in range(2):
            output_val = organism.feedforward([a, b])[0].output_val
            organism.fitness += abs(output_val - xor(a, b))


def simple_evaluate(organism):
    a, b = 1, 1
    output_val = organism.feedforward([a, b])[0].output_val
    organism.fitness += abs(output_val - xor(a, b)) * 100


def main():
    n = 100
    epochs = 200
    population = Population(n, 2, 1)

    # for i in range(1):
    #     print(population.organisms[i].feedforward([0, 0]))
    #     print(population.organisms[i].feedforward([1, 1]))
    #     print(population.organisms[i].feedforward([0, 1]))
    #     print(population.organisms[i].feedforward([1, 0]))
    #     print("-----------------------")

    count = 0
    for organism in population.organisms:
        population.add_node(organism)
        if count % 6 == 0:
            population.add_node(organism)
        count += 1

    for i in range(epochs):
        for organism in population.organisms:
            evaluate_log_and(organism)

        population.update_champion()

        # for i in range(10):
        #     print(round(population.organisms[i].fitness, 2))
        # print("----------------------")

        population.create_species()
        # for species in population.species:
        #     print(len(species.organisms))
        # print("-----------------")

        population.natural_selection()

        population.create_next_generation()
        # print(len(population.organisms))

        # if len(population.organisms) != 90:
        #     print(len(population.organisms))

        population.connections_history.clear()

    print("================================")
    for organism in population.organisms:
        evaluate_log_and(organism)
    population.update_champion()
    # for i in range(10):
    #     print(population.organisms[i].feedforward([1, 1]))
    #     print(population.organisms[i].feedforward([1, 0]))
    #     print("-----------------------")

    print(population.champion.feedforward([0, 0]))
    print(population.champion.feedforward([1, 1]))
    print(population.champion.feedforward([0, 1]))
    print(population.champion.feedforward([1, 0]))
    # print(population.species[0].representative.feedforward([1, 0]))
    # print(population.species[0].representative.feedforward([0, 1, 0]))
    print("FITNESS:", population.champion.fitness)
    population.champion.draw()
    print(population.champion.input_nodes)
    print(population.champion)


if __name__ == "__main__":
    main()
