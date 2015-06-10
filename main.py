#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
# -*- coding: utf-8 -*-
import numpy  # sudo apt-get install python-numpy
import random

# Matrix
# -------
# 9: Wall
# 8: Starting Point
# 7: Finish Point
# (1-6): Different obstacles
# 0: Walkable
FINISH_POINT = 7
STARTING_POINT = 8


class Chromosome():

    def __init__(self, x, y, step):
        self.x = x
        self.y = y
        self.step = step

    @property
    def position(self):
        return self.x, self.y


class Solution:

    X_DELTA_LIST = [1, 0, -1, 0]
    Y_DELTA_LIST = [0, 1, 0, -1]
    # Penalidad por pasar por un obstaculo, da mayor prefencia a soluciones sin obtáculos
    OBSTACLE_PENALTY = 1000

    def __init__(self, maze):
        self.chromosomes = []
        self.fitness = 99999
        self.position_x = maze.position_x
        self.position_y = maze.position_y
        self.matrix = maze.matrix

    # Make a solution for the maze and get fitness and sets the fitness
    def run(self):
        position = 0
        fitness = 0
        while position != FINISH_POINT:
            step = random.randint(0, 3)  # 0: DOWN, 1: RIGHT, 2: UP, 3: LEFT
            dx = self.X_DELTA_LIST[step]
            dy = self.Y_DELTA_LIST[step]
            try:
                position = self.matrix[self.position_x + dx][self.position_y + dy]

                fitness = fitness + 1 + position * self.OBSTACLE_PENALTY
                # actualizo la posicion actual
                self.position_x += dx
                self.position_y += dy
                # agrego los datos del cromosoma
                self.chromosomes.append(Chromosome(self.position_x, self.position_y, step))
            except IndexError as error:
                position = 0
        self.fitness = fitness


    # Get fitness for the solution    
    def get_fitness(self):
        return self.fitness

    # Print the solution in screen    
    def print_solution(self):
        # TODO: imprimir matriz resuelta
        print "Camino mínimo: " + ", ".join([str(chrom.position) for chrom in self.chromosomes])
        print "Direcciones: " + ", ".join([str(chrom.step) for chrom in self.chromosomes])


# Contains all the information about the Maze  and how to solve it
class Maze():

    # Define initials parameters
    def __init__(self, population, iterations):
        self.finish = False
        self.matrix = numpy.zeros(shape=(8, 8))
        self.population = []
        self.population_number = population
        self.iteration = 0
        self.max_iteration = iterations
        self.position_x = None
        self.position_y = None

    def set_stating_point(self):

        x = 0
        for row in self.matrix:
            y = 0
            for col in row:
                if col == STARTING_POINT:
                    self.position_x = x
                    self.position_y = y
                    break
                y += 1
            if self.position_x and self.position_y:
                break
            x += 1

    # Load the map with the access and exit point
    def load_map(self):
        # Hardcodear matris al principio, despues vemos si hacemos otra cosa
        for i in range(0, 8):
            self.matrix[i][0] = 9
        for j in range(0, 8):
            self.matrix[7][j] = 9
        for j in range(0, 8):
            self.matrix[0][j] = 9
        for i in range(0, 8):
            self.matrix[i][7] = 9
        self.matrix[3][6] = 7
        self.matrix[1][7] = 8
        self.matrix[2][2] = 1
        self.matrix[3][2] = 3
        self.matrix[4][3] = 6
        self.matrix[2][4] = 5
        self.matrix[2][5] = 4
        self.matrix[5][5] = 3
        self.matrix[2][6] = 2
        print self.matrix
        self.set_stating_point()

    # Creates the initial population
    def init_population(self):
        for i in range(self.population_number):
            a_solution = Solution(self)
            a_solution.run()
            # a_solution.print_solution()
            self.population.append(a_solution)

    # Evaluates if we arrived to a good solution
    def has_finished(self):
        if self.iteration >= self.max_iteration:
            self.finish = True
        # TODO: Dar un valor a self.best_posible
        # elif self.population[0].get_fitness() <= self.best_posible:
        #     self.finish = True
        return self.finish

    # Order the list by fitness
    def calc_fitness(self):
        self.population.sort(key=lambda solution: solution.get_fitness())

    # Mutates the solutions according to the
    # parameters passed on the init
    def mutate(self):
        pass
        # Mates the solutions according to the

    # parameters passed on the initialization
    def mate(self):
        pass


    # Return the solution with best fitness score
    def get_winner(self):
        return self.population[0]


def main():
    # TODO: pasar parámetros al constructor
    maze = Maze(25000, 1)
    maze.load_map()
    maze.init_population()
    maze.calc_fitness()
    while not maze.has_finished():
        maze.mutate()
        maze.mate()
        maze.calc_fitness()
        maze.iteration += 1
    winner = maze.get_winner()
    print maze.matrix
    winner.print_solution()


if __name__ == '__main__':
    main()
