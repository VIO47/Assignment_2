import time
from Maze import Maze
from PathSpecification import PathSpecification
from Ant import Ant

# Class representing the first assignment. Finds shortest path between two points in a maze according to a specific
# path specification.
class AntColonyOptimization:

    # Constructs a new optimization object using ants.
    # @param maze the maze .
    # @param antsPerGen the amount of ants per generation.
    # @param generations the amount of generations.
    # @param Q normalization factor for the amount of dropped pheromone
    # @param evaporation the evaporation factor.
    def __init__(self, maze, ants_per_gen, generations, q, evaporation):
        self.maze = maze
        self.ants_per_gen = ants_per_gen
        self.generations = generations
        self.q = q
        self.evaporation = evaporation

     # Loop that starts the shortest path process
     # @param spec Spefication of the route we wish to optimize
     # @return ACO optimized route
    def find_shortest_route(self, path_specification):
        shortest_route_overall = None
        self.maze.reset(self.q)
        for i in range(self.generations):
            routes = []
            for j in range(self.ants_per_gen):
                ant = Ant(self.maze, path_specification)
                # to do: use timeout instead of 100 iterations
                route = ant.find_route(100)
                if route != None:
                    routes.append(route)  
                    if route.shorter_than(shortest_route_overall):
                        shortest_route_overall = route
            self.maze.add_pheromone_routes(routes)
            self.maze.evaporate(self.evaporation)
            
        return shortest_route_overall