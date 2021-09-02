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
            organism.fitness += (output_val - xor(a, b)) ** 2


def simple_evaluate(organism):
    a, b = 1, 1
    output_val = organism.feedforward([a, b])[0].output_val
    organism.fitness += abs(output_val - xor(a, b)) * 100



def main():
    average_fitness = []
    champion_fitness = []

    n = 100
    epochs = 300
    population = Population(n, 2, 1)

    # count = 0

    # for organism in population.organisms:
    #     population.add_node(organism)
    #     population.add_node(organism)

    #     # for i in range(2):
    #     #     population.add_connection(organism)
    #     if count % 4 == 0:
    #         population.add_node(organism)
    #         # for i in range(2):
    #         #     population.add_connection(organism)
    #     # if count % 5 == 0:
    #     #     population.add_node(organism)
    #     #     population.add_connection(organism)
    #     #     population.add_connection(organism)
    #     count += 1

    for i in range(epochs):
        avg = 0.0
        for organism in population.organisms:
            evaluate_xor(organism)
            avg += organism.fitness
        average_fitness.append(avg/len(population.organisms))

        population.update_champion()
        champion_fitness.append(population.champion.fitness)

        population.create_species()
        # print(len(population.species))

        population.natural_selection()

        population.create_next_generation()

        population.connections_history.clear()

    print("================================")
    for organism in population.organisms:
        evaluate_xor(organism)
    population.update_champion()

    for a in range(2):
        for b in range(2):
            print([a, b], population.champion.feedforward([a, b]))

    print("FITNESS:", population.champion.fitness)
    population.champion.draw()
    print(population.champion.input_nodes)
    print(population.champion)

    plt.plot([i for i in range(epochs)], champion_fitness, color='y', label='champ')
    plt.plot([i for i in range(epochs)], average_fitness, color='b', label='avg')
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("Champion vs Average for xor")
    # # plt.xticks([i for i in range(0, epochs, 10)])
    plt.legend()
    plt.show()

    population.champion.save("xor_champ.json")


if __name__ == "__main__":
    main()
