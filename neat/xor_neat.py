import math

import numpy as np
from matplotlib import pyplot as plt
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
    average_fitness = []
    champion_fitness = []

    n = 100
    epochs = 200
    population = Population(n, 2, 1)

    count = 0
    for organism in population.organisms:
        population.add_node(organism)
        if count % 6 == 0:
            population.add_node(organism)
        count += 1

    for i in range(epochs):
        avg = 0.0
        for organism in population.organisms:
            evaluate_log_and(organism)
            avg += organism.fitness
        average_fitness.append(avg/len(population.organisms))

        population.update_champion()
        champion_fitness.append(population.champion.fitness)

        population.create_species()

        population.natural_selection()

        population.create_next_generation()
        for organism in population.organisms:
            organism.fitness = 0.0

        population.connections_history.clear()

    print("================================")
    for organism in population.organisms:
        evaluate_log_and(organism)
    population.update_champion()

    print(population.champion.feedforward([0, 0]))
    print(population.champion.feedforward([1, 1]))
    print(population.champion.feedforward([0, 1]))
    print(population.champion.feedforward([1, 0]))
    print("FITNESS:", population.champion.fitness)
    population.champion.draw()
    print(population.champion.input_nodes)
    print(population.champion)

    plt.plot([i for i in range(epochs)], average_fitness)
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("Average fitness for logical and")
    # plt.xticks([i for i in range(0, epochs, 10)])
    plt.show()
    print(average_fitness[170:180])


if __name__ == "__main__":
    main()
