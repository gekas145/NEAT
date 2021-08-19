from Population import Population
from numpy.random import binomial as bin


def xor(x, y, z):
    return (x + y + z) % 2


def evaluate(organism):
    for i in range(10):
        x, y, z = bin(3, 0.5)

        output_val = organism.feedforward([x, y, z])[0].output_val
        real_val = xor(x, y, z)

        if output_val < 0.5 and real_val == 0 or output_val > 0.5 and real_val == 1:
            organism.fitness += 1


def main():
    n = 100
    epochs = 30
    population = Population(n, 3, 1)

    for i in range(epochs):
        for organism in population.organisms:
            evaluate(organism)

        population.create_species()

        population.natural_selection()

        population.create_next_generation()

        population.erase_species()

        population.connections_history.clear()


if __name__ == "__main__":
    main()
