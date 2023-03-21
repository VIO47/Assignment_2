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
        self.visited = set()

    # Method that performs a single run through the maze by the ant.
    # @return The route the ant found through the maze.
    def find_route(self, iterations):
        route = Route(self.start)
        #current = self.start
        self.visited.add(self.start)
        it = 0

        while (self.current_position.__eq__(self.end) is False) and (it < iterations):
            i = self.current_position.x
            j = self.current_position.y

            sum_denominator = 0

            left = Coordinate(i - 1, j)
            up = Coordinate(i, j - 1)
            right = Coordinate(i + 1, j)
            down = Coordinate(i, j + 1)

            prob_north = 0
            prob_east = 0
            prob_south = 0
            prob_west = 0

            check_south = False
            check_north = False
            check_east = False
            check_west = False

            if self.maze.in_bounds(up) and self.maze.walls[up.x][up.y] == 1 and up not in self.visited:
                check_north = True
            if self.maze.in_bounds(right) and self.maze.walls[right.x][right.y] == 1 and right not in self.visited:
                check_east = True
            if self.maze.in_bounds(down) and self.maze.walls[down.x][down.y] == 1 and down not in self.visited:
                check_south = True
            if self.maze.in_bounds(left) and self.maze.walls[left.x][left.y] == 1 and left not in self.visited:
                check_west = True

            if(check_east == check_west == check_south == check_north == False):
                return None

            if check_north:
                sum_denominator += self.maze.pheromones[i][j - 1]
            if check_east:
                sum_denominator += self.maze.pheromones[i + 1][j]
            if check_south:
                sum_denominator += self.maze.pheromones[i][j + 1]
            if check_west:
                sum_denominator += self.maze.pheromones[i - 1][j]

            if check_north:
                prob_north = self.maze.pheromones[i][j - 1] / sum_denominator
            if check_east:
                prob_east = self.maze.pheromones[i + 1][j] / sum_denominator
            if check_south:
                prob_south = self.maze.pheromones[i][j + 1] / sum_denominator
            if check_west:
                prob_west = self.maze.pheromones[i - 1][j] / sum_denominator

            direction = self.rand.choices([Direction.north, Direction.east, Direction.south, Direction.west],
                                        [prob_north, prob_east, prob_south, prob_west])[0]

            #while(direction not in visited):
             #   direction = self.rand.choices([Direction.north, Direction.east, Direction.south, Direction.west],
              #                                [prob_north, prob_east, prob_south, prob_west])[0]
              #  iterations += 1

            if (direction == Direction.north):
                self.visited.add(up)
            if (direction == Direction.south):
                self.visited.add(down)
            if (direction == Direction.east):
                self.visited.add(right)
            if (direction == Direction.west):
                self.visited.add(left)

            route.add(direction)
            self.current_position = self.current_position.add_direction(direction)
            print(self.current_position)
            if self.current_position.__eq__(self.end):
                #print(route)
                return route
            it += 1

        return None
