import random
from Route import Route
from Direction import Direction
from Coordinate import Coordinate

#Class that represents the ants functionality.
class Ant:

    # Constructor for ant taking a Maze and PathSpecification.
    # @param maze Maze the ant will be running in.
    # @param spec The path specification consisting of a start coordinate and an end coordinate.
    def __init__(self, maze, path_specification):
        self.maze = maze
        self.start = path_specification.get_start()
        self.end = path_specification.get_end()
        self.current_position = self.start
        self.rand = random

    # Method that performs a single run through the maze by the ant.
    # @return The route the ant found through the maze.
    def find_route(self, iterations):
        route = Route(self.start)
        current = self.start
        i = current.x
        j = current.y
        it = 0

        while (current.__eq__(self.end) == False) and (it < iterations):
            sum_denominator = 0
            up = Coordinate(i - 1, j)
            right = Coordinate(i, j + 1)
            down = Coordinate(i + 1, j)
            left = Coordinate(i, j - 1)
            prob_north = 0
            prob_east = 0
            prob_south = 0
            prob_west = 0

            if self.maze.in_bounds(up):
                sum_denominator += self.maze.pheromones[i - 1][j]
            if self.maze.in_bounds(right):
                sum_denominator += self.maze.pheromones[i][j + 1]
            if self.maze.in_bounds(down):
                sum_denominator += self.maze.pheromones[i + 1][j]
            if self.maze.in_bounds(left):
                sum_denominator += self.maze.pheromones[i][j - 1]

            if self.maze.in_bounds(up):
                prob_north = self.maze.pheromones[i - 1][j] / sum_denominator
            if self.maze.in_bounds(right):
                prob_east = self.maze.pheromones[i][j + 1] / sum_denominator
            if self.maze.in_bounds(down):
                prob_south = self.maze.pheromones[i + 1][j] / sum_denominator
            if self.maze.in_bounds(left):
                prob_west = self.maze.pheromones[i][j - 1] / sum_denominator

            direction = self.rand.choices([Direction.north, Direction.east, Direction.south, Direction.west],
                                        [prob_north, prob_east, prob_south, prob_west])

            route.add(direction)
            current.add_direction(direction)
            if current.__eq__(self.end):
                return route
            it += 1

        return None
