import random

import numpy as np

from individual import Individual


class GeneticAlgorithm:
    def __init__(self, boxes, population_size=100, tournament_size=3):
        self.boxes = boxes
        self.population_size = population_size
        self.tournament_size = tournament_size
        self.population = [Individual() for _ in range(population_size)]

        for individual in self.population:
            individual.calculate_fitness(boxes)

    @staticmethod
    def hamming_distance(genome1, genome2):
        """
        Calculate the Hamming distance between two genomes (binary lists).
        Counts the number of positions where the genomes differ.

        :param genome1: First genome (binary list)
        :param genome2: Second genome (binary list)

        :return: Number of differing positions
        """
        if len(genome1) != len(genome2):
            raise ValueError("Genomes must be of equal length")

        return sum(g1 != g2 for g1, g2 in zip(genome1, genome2))

    def calculate_population_diversity(self):
        """
        Calculate the all-possible-pairs diversity measure for a population.
        :return: Diversity measure (sum of Hamming distances between all pairs)
        """
        diversity = 0
        population_size = len(self.population)

        for i in range(population_size):
            for j in range(i + 1, population_size):  # Start from i+1 to avoid counting pairs twice
                diversity += self.hamming_distance(self.population[i].genome, self.population[j].genome)

        return diversity

    def tournament_selection(self):
        """
        Selects a parent from a tournament
        :return: Winning Individual
        """
        # Randomly select tournament_size individuals
        competitors = random.sample(self.population, self.tournament_size)

        # Find the one with the highest fitness
        winner = max(competitors, key=lambda individual: individual.fitness)
        return winner

    def evolve(self, generations=100,
               crossover_rate=0.8, crossover_type='single', num_crossover_points=2,
               mutation_rate=1.0, mutation_type='multi', multi_mutation_rate=0.1):
        """
        Evolves the population for a specified number of generations.

        :param generations: Number of generations to evolve
        :param crossover_rate: Probability of crossover occurring
        :param crossover_type: 'single' or 'multi'
        :param num_crossover_points: Number of points for multi-point crossover
        :param mutation_rate: Probability of performing a mutation
        :param mutation_type: 'single' or 'multi'
        :param multi_mutation_rate:  Probability of each gene mutating (for multi_point)
        :return:
        """

        # Initialize arrays with zeros
        gens = np.arange(generations + 1)  # +1 for initial generation
        diversity_history = np.zeros(generations + 1)
        average_fitness_history = np.zeros(generations + 1)
        best_fitness_history = np.zeros(generations + 1)

        diversity_history[0] = self.calculate_population_diversity()
        average_fitness_history[0] = sum(individual.fitness for individual in self.population) / len(self.population)
        best_fitness_history[0] = max(individual.fitness for individual in self.population)

        for generation in range(generations):
            # Create new offspring
            offspring = []

            # Generate new individuals through selection, crossover, and mutation
            while len(offspring) < self.population_size:
                # Select parents using tournament selection
                parent1 = self.tournament_selection()
                parent2 = self.tournament_selection()

                # Apply crossover with some probability
                if random.random() < crossover_rate:
                    if crossover_type == 'single':
                        child1, child2 = Individual.single_point_crossover(parent1, parent2)
                    elif crossover_type == 'multi':
                        child1, child2 = Individual.multi_point_crossover(parent1, parent2, num_crossover_points)
                    else:
                        raise ValueError(f"Unknown crossover type: {crossover_type}")
                else:
                    # If no crossover, children are copies of parents
                    child1, child2 = Individual(parent1.genome.copy()), Individual(parent2.genome.copy())

                # Apply mutation
                if random.random() < mutation_rate:
                    if crossover_type == 'single':
                        child1.single_point_mutation()
                        child2.single_point_mutation()
                    elif crossover_type == 'multi':
                        child1.multi_point_mutation(multi_mutation_rate)
                        child2.multi_point_mutation(multi_mutation_rate)
                    else:
                        raise ValueError(f"Unknown mutation type: {mutation_type}")

                # Calculate fitness for the new offspring
                child1.calculate_fitness(self.boxes)
                child2.calculate_fitness(self.boxes)

                # Add offspring to the new population
                offspring.extend([child1, child2])

            # Ensure we have exactly population_size offspring
            offspring = offspring[:self.population_size]

            # Combine parents and offspring
            combined_population = self.population + offspring

            # Cull the population by 50% (keep the best individuals)
            combined_population.sort(key=lambda individual: individual.fitness, reverse=True)
            self.population = combined_population[:self.population_size]

            current_diversity = self.calculate_population_diversity()
            current_average_fitness = sum(individual.fitness for individual in self.population) / len(self.population)
            current_best_fitness = max(individual.fitness for individual in self.population)
            # Save initial values
            diversity_history[generation + 1] = current_diversity
            average_fitness_history[generation + 1] = current_average_fitness
            best_fitness_history[generation + 1] = current_best_fitness


            # Print statistics
            print(f"Generation {generation + 1}: Best Fitness = {current_best_fitness}, Average Fitness = {current_average_fitness}, Diversity = {current_diversity}")

        # Return the best individual found
        best_individual = max(self.population, key=lambda individual: individual.fitness)
        history = {
            "diversity": diversity_history,
            "average_fitness": average_fitness_history,
            "best_fitness": best_fitness_history,
            "generations": gens
        }
        return best_individual, history
