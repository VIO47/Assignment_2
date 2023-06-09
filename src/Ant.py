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
            #left = Coordinate(i, j - 1)
            #up = Coordinate(i - 1, j)
            #right = Coordinate(i, j + 1)
            #down = Coordinate(i + 1, j)
            prob_north = 0
            prob_east = 0
            prob_south = 0
            prob_west = 0
            pheromone_north = 0
            pheromone_east = 0
            pheromone_south = 0
            pheromone_west = 0


            check_south = False
            check_north = False
            check_east = False
            check_west = False

            if self.maze.in_bounds(up) and self.maze.walls[up.x][up.y] == 1:
                check_north = True
            if self.maze.in_bounds(right) and self.maze.walls[right.x][right.y] == 1:
                check_east = True
            if self.maze.in_bounds(down) and self.maze.walls[down.x][down.y] == 1:
                check_south = True
            if self.maze.in_bounds(left) and self.maze.walls[left.x][left.y] == 1 and left:
                check_west = True

            if(check_east == check_west == check_south == check_north == False):
                return None

            if check_north:
                pheromone_north = self.maze.pheromones[i][j - 1]
                if up in self.visited:
                    pheromone_north = pheromone_north * 0.5
                sum_denominator += pheromone_north
            if check_east:
                pheromone_east = self.maze.pheromones[i + 1][j]
                if right in self.visited:
                    pheromone_east = pheromone_east * 0.5
                sum_denominator += pheromone_east
            if check_south:
                pheromone_south = self.maze.pheromones[i][j + 1]
                if down in self.visited:
                    pheromone_south = pheromone_south * 0.5
                sum_denominator += pheromone_south
            if check_west:
                pheromone_west = self.maze.pheromones[i - 1][j]
                if left in self.visited:
                    pheromone_west = pheromone_west * 0.5
                sum_denominator += pheromone_west

            if check_north:
                prob_north = pheromone_north / sum_denominator
            if check_east:
                prob_east = pheromone_east / sum_denominator
            if check_south:
                prob_south = pheromone_south/ sum_denominator
            if check_west:
                prob_west = pheromone_west/ sum_denominator

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
            if self.current_position.__eq__(self.end):
                print("Found route")
                print(len(route.get_route()))
                return route
            it += 1

        return None
