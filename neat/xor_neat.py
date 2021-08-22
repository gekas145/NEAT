from Population import Population
from numpy.random import binomial as bin
from random import uniform
from math import floor


def xor(x, y):
    return (x + y) % 2

def evaluate(organism):
    # for j in range(10):
    #     x, y = bin(2, 0.5, size=2)
    #     output_val = organism.feedforward([x, y])[0].output_val
    #     real_val = xor(x, y)
    #     organism.fitness += (output_val - real_val) ** 2

    for a in range(2):
        for b in range(2):
            for i in range(100):
                output_val = organism.feedforward([a, b])[0].output_val
                organism.fitness += (output_val - xor(a, b)) ** 2




def main():
    n = 90
    epochs = 50
    population = Population(n, 2, 1)

    for i in range(10):
        print(population.organisms[i].feedforward([1, 1]))
        print(population.organisms[i].feedforward([1, 0]))
        print("-----------------------")

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

        population.erase_species()
        # print(len(population.organisms))

        population.connections_history.clear()

    population.organisms.sort(key=lambda x: x.fitness)
    print("================================")
    for i in range(10):
        print(population.organisms[i].feedforward([1, 1]))
        print(population.organisms[i].feedforward([1, 0]))
        print("-----------------------")
    # print(population.species[0].representative.feedforward([1, 1]))
    # print(population.species[0].representative.feedforward([1, 0]))
    # print(population.species[0].representative.feedforward([0, 1, 0]))
    population.organisms[0].draw()

if __name__ == "__main__":
    main()
