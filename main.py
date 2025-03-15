from box import Box
from display import print_solution, plot_genetic_algorithm_history
from genetic_algorithm import GeneticAlgorithm
from config import *

# Create the list of Box objects with weight and importance
boxes = [
    Box(20, 6),
    Box(30, 5),
    Box(60, 8),
    Box(90, 7),
    Box(50, 6),
    Box(70, 9),
    Box(30, 4),
    Box(30, 5),
    Box(70, 4),
    Box(20, 9),
    Box(20, 2),
    Box(60, 1)
]

# Initialize the GeneticAlgorithm with the list of boxes
ga = GeneticAlgorithm(boxes=boxes,
                      population_size=POPULATION_SIZE,
                      tournament_size=TOURNAMENT_SIZE)

# Evolve the population for a specified number of generations
best_solution, history  = ga.evolve(generations=GENERATIONS,
                                    crossover_type=CROSSOVER_TYPE,
                                    crossover_rate=CROSSOVER_RATE,
                                    num_crossover_points=NUM_CROSSOVER_POINTS,
                                    mutation_type=MUTATION_TYPE,
                                    mutation_rate=MUTATION_RATE,
                                    multi_mutation_rate=MUTATION_MULTI_RATE)

# Print the best solution and its details
print_solution(genome=best_solution.genome, boxes=boxes, max_weight=250)

# Create a plot of the genetic algorithm's history
plot_genetic_algorithm_history(history, filename='ga_history.png')