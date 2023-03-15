import random
import numpy as np
from TSPData import TSPData

# TSP problem solver using genetic algorithms.
class GeneticAlgorithm:

    # Constructs a new 'genetic algorithm' object.
    # @param generations the amount of generations.
    # @param popSize the population size.
    def __init__(self, generations, pop_size):
        self.generations = generations
        self.pop_size = pop_size

        # This method should solve the TSP.
        # @param pd the TSP data.
        # @return the optimized product sequence.

    def solve_tsp(self, tsp_data):
        self.tsp_data = tsp_data
        self.city_count = 18

        # Generate initial population
        self.population = self._generate_initial_population()

        # Loop through generations
        for i in range(self.generations):
            self._next_generation()

        # Return the best route
        return self._get_best_route()

    # Generates the initial population randomly.
    def _generate_initial_population(self):
        population = []
        for i in range(self.pop_size):
            population.append(random.sample(range(self.city_count), self.city_count))
        return population

        # Returns the fitness of a route. Fitness is the inverse of the route length.

    def _fitness(self, route):
        length = self._get_route_distance(route)
        if length == 0:
            return float('inf')
        return 1.0 / length

        # Returns the length of a route.

    def _route_length(self, route):
        length = 0.0
        for i in range(self.city_count):
            j = (i + 1) % self.city_count
            #city_i = self.tsp_data.distances[route[i]][route[j]]
            #city_j = self.tsp_data.distances[route[j]]
            #print(city_j)
            #length += self._distance(city_i, city_j)
            length += self.tsp_data.distances[route[i]][route[j]]
        return length

        # Calculates the Euclidean distance between two cities.

    def _distance(self, city_a, city_b):
        return np.linalg.norm(city_a - city_b)

        # Generates the next generation.

    def _next_generation(self):
        new_population = []
        for i in range(self.pop_size):
            parent_a = self._select_parent()
            parent_b = self._select_parent()
            child = self._crossover(parent_a, parent_b)
            new_population.append(child)
            #new_population.append(child2)
        self.population = new_population

        # Selects a parent for breeding.

    def _select_parent(self):
        probabilities = []
        for citizen in self.population:
            probabilities.append(1 - self._fitness(citizen))
        norm = np.linalg.norm(probabilities)
        index = np.arange(0, self.pop_size)
        vector = probabilities/norm if norm != 0 else probabilities
        chosen = random.choices(index, (probabilities / norm))
        return self.population[chosen[0]]

        # Performs crossover between two parents.

    def _crossover(self, parent_a, parent_b):
        # Perform crossover with 2-point crossover
        cut1 = random.randint(0, self.city_count - 2)
        cut2 = random.randint(cut1, self.city_count - 1)

        # Create a child
        child = parent_b
        #child2 = [-1] * self.city_count
        #child2 = parent_a

        # Copy the middle segment from parent A
        child[cut1:cut2 + 1] = parent_a[cut1:cut2]

        #child2[cut1:cut2 + 1] = parent_b[cut1:cut2]

        # Fill the remaining positions with cities from parent B, in order
        p_b_index = 0
        #for i in range(self.city_count):
        #    if child[i] == -1:
        #        while parent_b[p_b_index] in child:
        #            p_b_index += 1
        #        child[i] = parent_b[p_b_index]
        #        p_b_index += 1

        return child

    def _get_best_route(self):
        best_route = None
        best_distance = float('inf')

        for route in self.population:
            distance = self._get_route_distance(route)

            if distance < best_distance:
                best_distance = distance
                best_route = route

        return best_route, best_distance

    def _get_route_distance(self, route):
        distance = 0
        distances = self.tsp_data.distances
        for i in range(len(route)):
            from_city = route[i]
            to_city = route[0] if i == len(route) - 1 else route[i + 1]
            distance += distances[from_city][to_city]
        return distance