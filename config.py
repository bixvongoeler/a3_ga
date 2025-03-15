# Configuration file for the Genetic Algorithm

# Number of Individuals in each Generation
POPULATION_SIZE = 50
# Size of tournament for parent selection
TOURNAMENT_SIZE = 4
# Number of generations to run the algorithm for
GENERATIONS = 20
# Crossover type: 'single' for single point, 'multi' for multipoint
CROSSOVER_TYPE = 'single'
# Probability of a crossover between two parents
CROSSOVER_RATE = 0.90
# Number of crossover points for multipoint crossover
NUM_CROSSOVER_POINTS = 2
# Mutation type: 'single' for single point, 'multi' for multipoint
MUTATION_TYPE = 'multi'
# Probability of a mutation occurring in each offspring
MUTATION_RATE = 0.9
# Probability of each bit mutating in multipoint mutation
MUTATION_MULTI_RATE = 0.3