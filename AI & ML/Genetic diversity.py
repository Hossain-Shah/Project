import random
import numpy as np
import matplotlib.pyplot as plt


def create_reference_solution(chromosome_length):
    number_of_ones = int(chromosome_length / 2)
    reference = np.zeros(chromosome_length)
    reference[0: number_of_ones] = 1
    np.random.shuffle(reference)
    return reference


print(create_reference_solution(70))


def create_starting_population(individuals, chromosome_length):
    population = np.zeros((individuals, chromosome_length))
    for i in range(individuals):
        ones = random.randint(0, chromosome_length)
        population[i, 0:ones] = 1
        np.random.shuffle(population[i])
    return population


print(create_starting_population(4, 10))


def calculate_fitness(reference, population):
    identical_to_reference = population == reference
    fitness_scores = identical_to_reference.sum(axis=1)
    return fitness_scores


reference = create_reference_solution(10)
print ('Reference solution: \n', reference)
population = create_starting_population(6, 10)
print ('\nStarting population: \n', population)
scores = calculate_fitness(reference, population)
print('\nScores: \n', scores)


def select_individual_by_tournament(population, scores):
    population_size = len(scores)
    fighter_1 = random.randint(0, population_size - 1)
    fighter_2 = random.randint(0, population_size - 1)
    fighter_1_fitness = scores[fighter_1]
    fighter_2_fitness = scores[fighter_2]
    if fighter_1_fitness >= fighter_2_fitness:
        winner = fighter_1
    else:
        winner = fighter_2
    return population[winner, :]


reference = create_reference_solution(10)
population = create_starting_population(6, 10)
scores = calculate_fitness(reference, population)
parent_1 = select_individual_by_tournament(population, scores)
parent_2 = select_individual_by_tournament(population, scores)
print(parent_1)
print(parent_2)


def breed_by_crossover(parent_1, parent_2):
    chromosome_length = len(parent_1)
    crossover_point = random.randint(1, chromosome_length - 1)
    child_1 = np.hstack((parent_1[0:crossover_point],
                         parent_2[crossover_point:]))
    child_2 = np.hstack((parent_2[0:crossover_point],
                         parent_1[crossover_point:]))
    return child_1, child_2


reference = create_reference_solution(15)
population = create_starting_population(100, 15)
scores = calculate_fitness(reference, population)
parent_1 = select_individual_by_tournament(population, scores)
parent_2 = select_individual_by_tournament(population, scores)
child_1, child_2 = breed_by_crossover(parent_1, parent_2)
print('Parents')
print(parent_1)
print(parent_2)
print('Children')
print(child_1)
print(child_2)


def randomly_mutate_population(population, mutation_probability):
    random_mutation_array = np.random.random(
        size=(population.shape))
    random_mutation_boolean = \
        random_mutation_array <= mutation_probability
    population[random_mutation_boolean] = \
        np.logical_not(population[random_mutation_boolean])
    return population


reference = create_reference_solution(15)
population = create_starting_population(100, 15)
scores = calculate_fitness(reference, population)
parent_1 = select_individual_by_tournament(population, scores)
parent_2 = select_individual_by_tournament(population, scores)
child_1, child_2 = breed_by_crossover(parent_1, parent_2)
population = np.stack((child_1, child_2))
mutation_probability = 0.25
print("Population before mutation")
print(population)
population = randomly_mutate_population(population, mutation_probability)
print("Population after mutation")
print(population)
chromosome_length = 75
population_size = 500
maximum_generation = 200
best_score_progress = []
reference = create_reference_solution(chromosome_length)
population = create_starting_population(population_size, chromosome_length)
scores = calculate_fitness(reference, population)
best_score = np.max(scores) / chromosome_length * 100
print('Starting best score, percent target: %.1f' % best_score)
best_score_progress.append(best_score)
for generation in range(maximum_generation):
    new_population = []
    for i in range(int(population_size / 2)):
        parent_1 = select_individual_by_tournament(population, scores)
        parent_2 = select_individual_by_tournament(population, scores)
        child_1, child_2 = breed_by_crossover(parent_1, parent_2)
        new_population.append(child_1)
        new_population.append(child_2)
    population = np.array(new_population)
    mutation_rate = 0.002
    population = randomly_mutate_population(population, mutation_rate)
    scores = calculate_fitness(reference, population)
    best_score = np.max(scores) / chromosome_length * 100
    best_score_progress.append(best_score)
print('End best score, percent target: %.1f' % best_score)
plt.plot(best_score_progress)
plt.xlabel('Generation')
plt.ylabel('Best score (% target)')
plt.show()