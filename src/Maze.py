import traceback
import sys

# Class that holds all the maze data. This means the pheromones, the open and blocked tiles in the system as
# well as the starting and end coordinates.
class Maze:

    # Constructor of a maze
    # @param walls int array of tiles accessible (1) and non-accessible (0)
    # @param width width of Maze (horizontal)
    # @param length length of Maze (vertical)
    def __init__(self, walls, width, length):
        self.walls = walls
        self.length = length
        self.width = width
        self.start = None
        self.end = None
        self.pheromones = None

    # Initialize pheromones to a start value.
    def initialize_pheromones(self, q):
        self.pheromones = []
        for x in range(self.width):
            self.pheromones.append([])
        
        for y in range(self.length):
            for x in range(self.width):
                if self.walls[x][y] == 1:
                    self.pheromones[x].append(q)
                else:
                    self.pheromones[x].append(0)

    # Reset the maze for a new shortest path problem.
    def reset(self, q):
        self.initialize_pheromones(q)

    # Update the pheromones along a certain route according to a certain Q
    # @param r The route of the ants
    # @param Q Normalization factor for amount of dropped pheromone
    def add_pheromone_route(self, route, q):
        if(route is not None):
            # current = route.start
            # if self.walls[current.x][current.y] == 1:
            #     new_pheromones = self.get_pheromone(current) + self.get_surrounding_pheromone(current)
            #     self.pheromones[current.x][current.y] = new_pheromones
            # else:
            #     self.pheromones[current.x][current.y] = 0
            #
            # for direction in route.route:
            #     if self.walls[current.x][current.y] == 1:
            #         current = current.add_direction(direction)
            #         new_pheromones = self.get_pheromone(current) + self.get_surrounding_pheromone(current) * (1 / len(route.route))
            #         self.pheromones[current.x][current.y] = new_pheromones
            #     else:
            #         self.pheromones[current.x][current.y] = 0
            current = route.start
            if(self.walls[current.x][current.y] == 1):
                self.pheromones[current.x][current.y] += q / len(route.route)
            else:
                self.pheromones[current.x][current.y] = 0
            for coord in route.route:
                current = current.add_direction(coord)
                if(self.walls[current.x][current.y] == 1):
                    self.pheromones[current.x][current.y] += q / len(route.route)
                else:
                    self.pheromones[current.x][current.y] = 0


     # Update pheromones for a list of routes
     # @param routes A list of routes
     # @param Q Normalization factor for amount of dropped pheromone
    def add_pheromone_routes(self, routes, q):
        for r in routes:
            self.add_pheromone_route(r, q)

    # Evaporate pheromone
    # @param rho evaporation factor
    def evaporate(self, rho):
        for i in range(len(self.pheromones)):
            for j in range(len(self.pheromones[0])):
                self.pheromones[i][j] *= (1 - rho)

    # Width getter
    # @return width of the maze
    def get_width(self):
        return self.width

    # Length getter
    # @return length of the maze
    def get_length(self):
        return self.length

    # Returns the amount of pheromones on the neighbouring positions (N/S/E/W).
    # @param position The position to check the neighbours of.
    # @return the pheromones of the neighbouring positions.
    def get_surrounding_pheromone(self, position):
        sum_pheromones = 0
        i = position.x
        j = position.y

        if(i > 0 and self.walls[i - 1][j] == 1):
            sum_pheromones += self.pheromones[i - 1][j]
        if(i < self.width - 1 and self.walls[i + 1][j] == 1):
            sum_pheromones += self.pheromones[i + 1][j]
        if(j > 0 and self.walls[i][j - 1] == 1):
            sum_pheromones += self.pheromones[i][j - 1]
        if(j < self.length - 1 and self.walls[i][j + 1] == 1):
            sum_pheromones += self.pheromones[i][j + 1]

        return sum_pheromones

    # Pheromone getter for a specific position. If the position is not in bounds returns 0
    # @param pos Position coordinate
    # @return pheromone at point
    def get_pheromone(self, pos):
        if self.in_bounds(pos):
            return self.pheromones[pos.x][pos.y]
        else:
            return 0
        

    # Check whether a coordinate lies in the current maze.
    # @param position The position to be checked
    # @return Whether the position is in the current maze
    def in_bounds(self, position):
        return position.x_between(0, self.width) and position.y_between(0, self.length)

    # Representation of Maze as defined by the input file format.
    # @return String representation
    def __str__(self):
        string = ""
        string += str(self.width)
        string += " "
        string += str(self.length)
        string += " \n"
        for y in range(self.length):
            for x in range(self.width):
                string += str(self.walls[x][y])
                string += " "
            string += "\n"
        return string

    # Method that builds a mze from a file
    # @param filePath Path to the file
    # @return A maze object with pheromones initialized to 0's inaccessible and 1's accessible.
    @staticmethod
    def create_maze(file_path):
        try:
            f = open(file_path, "r")
            lines = f.read().splitlines()
            dimensions = lines[0].split(" ")
            width = int(dimensions[0])
            length = int(dimensions[1])
            
            #make the maze_layout
            maze_layout = []
            for x in range(width):
                maze_layout.append([])
            
            for y in range(length):
                line = lines[y+1].split(" ")
                for x in range(width):
                    if line[x] != "":
                        state = int(line[x])
                        maze_layout[x].append(state)
            print("Ready reading maze file " + file_path)
            return Maze(maze_layout, width, length)
        except FileNotFoundError:
            print("Error reading maze file " + file_path)
            traceback.print_exc()
            sys.exit()