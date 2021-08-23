from Population import Population
from numpy.random import binomial as bin
from random import uniform
from math import floor


def xor(x, y):
    return (x + y) % 2

def evaluate(organism):
    for a in range(2):
        for b in range(2):
            for i in range(80):
                output_val = organism.feedforward([a, b])[0].output_val
                organism.fitness += abs(output_val - xor(a, b))




def main():
    n = 120
    epochs = 80
    population = Population(n, 2, 1)

    # for i in range(10):
    #     print(population.organisms[i].feedforward([1, 1]))
    #     print(population.organisms[i].feedforward([1, 0]))
    #     print("-----------------------")

    # for organism in population.organisms:
    #     if uniform(0, 1) < 0.3:
    #         population.add_node(organism)
    #     if uniform(0, 1) < 0.7:
    #         population.add_node(organism)

    for i in range(epochs):
        for organism in population.organisms:
            evaluate(organism)

        # for i in range(10):
        #     print(round(population.organisms[i].fitness, 2))
        # print("----------------------")

        population.create_species()

        population.natural_selection()

        population.create_next_generation()
        # print(len(population.organisms))

        population.erase_species()
        # if len(population.organisms) != 90:
        #     print(len(population.organisms))

        population.connections_history.clear()

    print("================================")
    for organism in population.organisms:
        evaluate(organism)
    population.organisms.sort(key=lambda x: x.fitness)
    # for i in range(10):
    #     print(population.organisms[i].feedforward([1, 1]))
    #     print(population.organisms[i].feedforward([1, 0]))
    #     print("-----------------------")

    print(population.organisms[0].feedforward([1, 1]))
    print(population.organisms[0].feedforward([1, 0]))
    print(population.organisms[0].feedforward([0, 1]))
    print(population.organisms[0].feedforward([0, 0]))
    # print(population.species[0].representative.feedforward([1, 0]))
    # print(population.species[0].representative.feedforward([0, 1, 0]))
    print("FITNESS:", population.organisms[0].fitness)
    population.organisms[0].draw()

if __name__ == "__main__":
    main()
