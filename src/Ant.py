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
        self.visited = []

    # Method that performs a single run through the maze by the ant.
    # @return The route the ant found through the maze.
    def find_route(self, iterations):
        route = Route(self.start)
        current = self.start
        self.visited.append(self.start)
        it = 0

        while (current.__eq__(self.end) is False) and (it < iterations):
            i = current.x
            j = current.y

            sum_denominator = 0
            left = Coordinate(i - 1, j)
            up = Coordinate(i, j - 1)
            right = Coordinate(i + 1, j)
            down = Coordinate(i, j + 1)
            #left = Coordinate(i, j - 1)
            #up = Coordinate(i - 1, j)
            #right = Coordinate(i, j + 1)
            #down = Coordinate(i + 1, j)
            prob_north = 0
            prob_east = 0
            prob_south = 0
            prob_west = 0

            if self.maze.in_bounds(up) and up not in self.visited and self.maze.walls[up.x][up.y] == 1:
                sum_denominator += self.maze.pheromones[i][j + 1]

            print(right)
            if self.maze.in_bounds(right) and right not in self.visited and self.maze.walls[right.x][right.y] == 1:
                sum_denominator += self.maze.pheromones[i + 1][j]
            if self.maze.in_bounds(down) and down not in self.visited and self.maze.walls[down.x][down.y] == 1:
                sum_denominator += self.maze.pheromones[i][j - 1]
            if self.maze.in_bounds(left) and left not in self.visited and self.maze.walls[left.x][left.y] == 1:
                sum_denominator += self.maze.pheromones[i - 1][j]

            #print(sum_denominator)
            if (sum_denominator == 0):
                return None

            if self.maze.in_bounds(up) and up not in self.visited and self.maze.walls[up.x][up.y] == 1:
                prob_north = self.maze.pheromones[i][j + 1] / sum_denominator
            if self.maze.in_bounds(right) and right not in self.visited and self.maze.walls[right.x][right.y] == 1:
                prob_east = self.maze.pheromones[i + 1][j] / sum_denominator
            if self.maze.in_bounds(down) and down not in self.visited and self.maze.walls[down.x][down.y] == 1:
                prob_south = self.maze.pheromones[i][j - 1] / sum_denominator
            if self.maze.in_bounds(left) and left not in self.visited and self.maze.walls[left.x][left.y] == 1:
                prob_west = self.maze.pheromones[i - 1][j] / sum_denominator

            direction = self.rand.choices([Direction.north, Direction.east, Direction.south, Direction.west],
                                        [prob_north, prob_east, prob_south, prob_west])[0]

            #while(direction not in visited):
             #   direction = self.rand.choices([Direction.north, Direction.east, Direction.south, Direction.west],
              #                                [prob_north, prob_east, prob_south, prob_west])[0]
              #  iterations += 1

            if (direction == Direction.north):
                self.visited.append(up)
            if (direction == Direction.south):
                self.visited.append(down)
            if (direction == Direction.east):
                self.visited.append(right)
            if (direction == Direction.west):
                self.visited.append(left)

            print(direction)
            route.add(direction)
            current.add_direction(direction)
            if current.__eq__(self.end):
                print(route)
                return route
            it += 1

        return None
