from matplotlib import pyplot as plt
from Population import Population
from pole_balancing.progress_bar import printProgressBar


def xor(x, y):
    return (x + y) % 2


def evaluate_xor(organism):
    fitness = 4
    for a in range(2):
        for b in range(2):
            output_val = organism.feedforward([a, b])[0].output_val
            fitness -= (output_val - xor(a, b)) ** 2
    organism.fitness = -fitness  # minus sign because of sorting in natural selection specifics


def main():
    average_fitness = []
    champion_fitness = []

    n = 100
    epochs = 300
    population = Population(n, 2, 1)
    print_progress_bar = True
    save_champ_path = "xor_champ.json"

    if print_progress_bar:
        printProgressBar(0, epochs, prefix='Progress:', suffix='Complete', length=50)

    for i in range(epochs):
        avg = 0.0
        for organism in population.organisms:
            evaluate_xor(organism)
            avg -= organism.fitness  # minus sign because algorithm uses negative fitness
        average_fitness.append(avg/len(population.organisms))

        population.update_champion()
        champion_fitness.append(-population.champion.fitness)

        population.create_species()

        population.natural_selection()

        population.create_next_generation()

        population.connections_history.clear()

        if print_progress_bar:
            printProgressBar(i + 1, epochs, prefix='Progress:', suffix='Complete', length=50)

    for organism in population.organisms:
        evaluate_xor(organism)
    population.update_champion()

    plt.plot([i for i in range(epochs)], champion_fitness, color='y', label='champ')
    plt.plot([i for i in range(epochs)], average_fitness, color='b', label='avg')
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("Champion vs Average for xor")
    plt.legend()
    plt.show()

    population.champion.save(save_champ_path)


if __name__ == "__main__":
    main()
