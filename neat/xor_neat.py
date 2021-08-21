from Population import Population
from numpy.random import binomial as bin


def xor(x, y, z):
    return (x + y + z) % 2





def main():
    n = 100
    epochs = 5
    population = Population(n, 3, 1)
    # print(population.organisms[0].feedforward([0, 0, 0]))

    for i in range(epochs):
        for organism in population.organisms:
            for j in range(10):
                x, y, z = bin(3, 0.5, size=3)
                output_val = organism.feedforward([x, y, z])[0].output_val
                real_val = xor(x, y, z)
                organism.fitness += (output_val - real_val) ** 2

            organism.fitness *= -1

        population.create_species()
        # print("----------------------------")
        # for species in population.species:
        #     print(len(species.organisms))

        population.natural_selection()

        print("----------------------------")
        for species in population.species:
            print(species.representative.fitness)

        population.create_next_generation()

        population.erase_species()

        population.connections_history.clear()

    print(population.species[0].representative.feedforward([1, 1, 1]))
    print(population.species[0].representative.feedforward([1, 0, 1]))
    print(population.species[0].representative.feedforward([1, 1, 0]))
    print(population.species[0].representative.feedforward([0, 1, 0]))
    print(population.species[0].representative.fitness)
    population.species[0].representative.draw()

if __name__ == "__main__":
    main()
