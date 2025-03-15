import numpy as np


def print_solution(genome, boxes, max_weight=250):
    """
    Prints a formatted representation of the solution genome.

    :param genome: Binary list representing which boxes are included
    :param boxes: List of Box objects with weight and importance
    :param max_weight: Maximum weight capacity of the knapsack
    """

    total_weight = 0
    total_importance = 0
    included_boxes = []

    # Calculate totals and collect included boxes
    for i, include in enumerate(genome):
        if include:
            box = boxes[i]
            total_weight += box.weight
            total_importance += box.importance
            included_boxes.append(f"#{i + 1}")


    # Check if solution is valid
    is_valid = total_weight <= max_weight

    # Print header
    print("\n" + "=" * 50)
    print(f"{' KNAPSACK SOLUTION ':^50}")
    print("=" * 50)

    # Print solution summary
    print(f"{'Solution Status:':<20} {'VALID' if is_valid else 'INVALID (Exceeds weight limit)'}")
    print(f"{'Total Weight:':<20} {total_weight} / {max_weight} ({(total_weight / max_weight * 100):.1f}%)")
    print(f"{'Total Importance:':<20} {total_importance}")

    # Print included boxes - simplified
    print(f"{'Genome:':<20} {''.join(map(str, genome))}")
    print(f"{'Included Boxes:':<20} {', '.join(map(str, included_boxes))}")

    print("=" * 50 + "\n")


def plot_genetic_algorithm_history(history, filename='ga_history.png'):
    try:
        import matplotlib.pyplot as plt

        diversity = history['diversity']
        avg_fitness = history['average_fitness']
        best_fitness = history['best_fitness']
        generations = history['generations']

        # Create figure and primary axis
        fig, ax1 = plt.subplots(figsize=(9, 6))

        # Plot fitness metrics on primary axis
        ax1.plot(generations, best_fitness, 'b-', linewidth=2, label='Best Fitness')
        ax1.plot(generations, avg_fitness, 'g--', linewidth=2, label='Average Fitness')
        ax1.set_xlabel('Generation', fontsize=12)
        ax1.set_ylabel('Fitness Value', fontsize=12, color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.set_ylim(bottom=25, top=45)  # Set y-axis to start from 0
        ax1.set_xlim(left=0, right=max(generations))  # Set x-axis to start from 0
        # Set x-axis ticks to show every generation
        ax1.set_xticks(np.arange(min(generations), max(generations) + 1, 1))
        ax1.set_yticks(np.arange(25, 45, 1))  # Set y-axis ticks to show every 2 units
        if len(generations) > 15:
            plt.xticks(rotation=45)


        # Create secondary y-axis for diversity
        ax2 = ax1.twinx()

        # Plot diversity on secondary axis
        color = 'red'
        ax2.plot(generations, diversity, color=color, linestyle='-.', linewidth=2, label='APP Diversity')
        ax2.set_ylabel('All-Possible-Pairs Diversity', fontsize=12, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        # Add title
        plt.title('Fitness and Diversity Evolution Across Generations', fontsize=14)

        # Add grid
        ax1.grid(True, linestyle='--', alpha=0.7)

        # Combine legends from both axes
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='center right', fontsize=10)

        # Adjust layout and save
        # plt.tight_layout()

        plt.show()
        fig.savefig(filename)
    except ImportError:
        print("matplotlib is not installed. Skipping plot generation.")
        print("To install matplotlib, run 'pip install matplotlib'.")
