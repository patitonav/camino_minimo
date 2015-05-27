#   Main.py

class solution:
    def __init__(self, matrix):
        self.chromozones = []
        self.run(matrix)
    
    # Make a solution  for the maze
    def run(self, matrix):
        return
    
    # Print the solution in screen    
    def print_solution(self):
        return

# Contains all the information about the Maze 
# and how to solve it
class Maze:
    # Define initials parameters
    def __init__(self):
        self.finish =  false
        self.matrix = [[]]
        self.population = []
    # Load the map with the access and exit point
    def loadMap(self):
        # Hardcodear matris al principio, despues vemos si hacemos otra cosa
        return
    # Creates the initial population
    def init_population(self):
        return
    # Return the value of the finish flag
    def finish(self):
        return false
    # Calculates the fitness of every solution
    # Order the list by fitness
    def calc_fitness(self):
        return
    # Mutates the solutions according to the 
    # parameters passed on the init
    def mutate(self):
        return 
    # Mates the solutions according to the 
    # parameters passed on the init
    def mate(self):
        return 
    # Return the solution con best fitness score
    def getWinner(self):
        return self.population[1]
    
def main():
    maze = Maze()
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