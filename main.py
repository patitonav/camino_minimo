#   Main.py

# Matrix
#-------
# 9: Wall
# 8: Starting Point
# 7: Finish Point
# (1-6): Diferent obstacles
# 0: Walkable
class solution:
    def __init__(self, matrix):
        self.chromozones = []
        self.fitness = 99999
        self.position_x
        self.position_y
        self.run(matrix)
    
    # Make a solution for the maze and get fitness
    # and sets the fitness
    def run(self, matrix):
        self.set_statingPoint()
        position =  0
        self.fitness = 0
        while (position != 7):
            step = random.randint(0, 3)
            #Goes Right
            if (step == 0) and(matrix[self.position_x+1][self.position_y] != 9):
                position = matrix[self.position_x+1][self.position_y]
                self.fitness = self.fitness + 1 + position
                self.chromozones.append(step)
            #Goes Up
            if (step == 0) and(matrix[self.position_x][self.position_y+1] != 9):
                position = matrix[self.position_x][self.position_y+1]
                self.fitness = self.fitness + 1 + position
                self.chromozones.append(step)
            #Goes Left
            if (step == 0) and(matrix[self.position_x-1][self.position_y] != 9):
                position = matrix[self.position_x-1][self.position_y]
                self.fitness = self.fitness + 1 + position
                self.chromozones.append(step)   
            #Goes Down
            if (step == 0) and(matrix[self.position_x][self.position_y-1] != 9):
                position = matrix[self.position_x][self.position_y-1]
                self.fitness = self.fitness + 1 + position
                self.chromozones.append(step)
            
        return
    
    # Finds and set the stating position    
    def set_statingPoint(self):
        return
    # Get fitness for the solution    
    def get_fitness(self):
        return self.fitness

    # Print the solution in screen    
    def print_solution(self):
        return

# Contains all the information about the Maze 
# and how to solve it
class maze:
    # Define initials parameters
    def __init__(self, population, iterations):
        self.finish =  false
        self.matrix = [[]]
        self.population = []
        self.population_number = population
        self.iteration = 0
        self.max_iteration = iterations
    # Load the map with the access and exit point
    def loadMap(self):
        # Hardcodear matris al principio, despues vemos si hacemos otra cosa
        return
    # Creates the initial population
    def init_population(self):
        for i in range(self.population_number):
            self.population.append(solution(self.matrix))
        return
    # Evaluates if we arrived to a good solution
    def finish(self):
        if self.iteration == self.max_iteration:
            self.finish = true
        if self.population[0].get_fitness <= self.best_posible:
            self.finish = true
        return self.finish
    # Order the list by fitness
    def calc_fitness(self):
        self.population.sort(key = get_fitness())
        return
    # Mutates the solutions according to the 
    # parameters passed on the init
    def mutate(self):
        return 
    # Mates the solutions according to the 
    # parameters passed on the initialization
    def mate(self):
        return 
    # Return the solution with best fitness score
    def getWinner(self):
        return self.population[0]
    
def main():
    maze = maze()
    maze.loadMap()
    maze.init_population()
    maze.calc_fitness()
    while (maze.finish() == false):
        maze.mutate()
        maze.mate()
        maze.calc_fitness()
    winner = maze.getWinner()
    winner.print_solution()
if __name__ == '__main__':
    main()