import random


class Individual:

    def __init__(self, genome=None):
        """
        Create a new individual
        :param genome: Generates a random genome if none provided
        """
        self.genome = genome if genome is not None else [random.randint(0, 1) for _ in range(12)]
        self.fitness = None

    def calculate_fitness(self, boxes, max_weight=250):
        """
        Calculate an individuals fitness given the set of boxes
        :param boxes: A list of boxes containing weight and importance vals
        :param max_weight: The maxium allowed knapsack weight
        :return: the individuals fitness value
        """
        total_weight = 0
        total_importance = 0

        for i, include in enumerate(self.genome):
            if include:
                total_weight += boxes[i].weight
                total_importance += boxes[i].importance

        # If weight exceeds limit, fitness is negative of the excess weight
        if total_weight > max_weight:
            self.fitness = max_weight - total_weight
        else:
            self.fitness = total_importance

        return self.fitness

    def single_point_mutation(self):
        """
        Mutate a single randomly selected bit in genome
        """
        mutation_point = random.randint(0, len(self.genome) - 1)
        self.genome[mutation_point] = 1 - self.genome[mutation_point]

    def multi_point_mutation(self, mutation_rate=0.1):
        '''
        Mutate a random selection of bits in genome
        :param mutation_rate: The probability of each bit mutating
        '''
        for i in range(len(self.genome)):
            if random.random() < mutation_rate:
                # Flip bit (0->1 or 1->0)
                self.genome[i] = 1 - self.genome[i]

    @staticmethod
    def single_point_crossover(parent1, parent2):
        """
        Performs a single point crossover between two parents
        :param parent1: An Individual
        :param parent2: An Individual
        :return: The two resulting child individuals
        """
        crossover_point = random.randint(1, len(parent1.genome) - 1)
        child1_genome = parent1.genome[:crossover_point] + parent2.genome[crossover_point:]
        child2_genome = parent2.genome[:crossover_point] + parent1.genome[crossover_point:]

        return Individual(child1_genome), Individual(child2_genome)

    @staticmethod
    def multi_point_crossover(parent1, parent2, num_points=2):
        '''
        Performs a multi point crossover between two parents
        :param parent1: An Individual
        :param parent2: An Individual
        :param num_points: The number of crossover divisions (value of 1 equivalent to single point xover)
        :return: The two resulting child individuals
        '''

        genome_length = len(parent1.genome)
        num_points = min(num_points, genome_length - 1)

        # Generate crossover points
        points = sorted(random.sample(range(1, genome_length), num_points))

        # Initialize child genomes
        child1_genome = []
        child2_genome = []

        # Start with first parent as source for both children
        source1, source2 = parent1.genome, parent2.genome

        # Add crossover points at beginning and end for easier processing
        all_points = [0] + points + [genome_length]

        # Create children by alternating segments between crossover points
        for i in range(len(all_points) - 1):
            start = all_points[i]
            end = all_points[i + 1]

            # If i is even, use source1 for child1 and source2 for child2
            # If i is odd, swap the sources
            if i % 2 == 0:
                child1_genome.extend(source1[start:end])
                child2_genome.extend(source2[start:end])
            else:
                child1_genome.extend(source2[start:end])
                child2_genome.extend(source1[start:end])

        return Individual(child1_genome), Individual(child2_genome)
