#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

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

    def __eq__(self, other):
        if isinstance(other, Chromosome):
            return self.position == other.position
        else:
            return NotImplemented


class Solution:

    X_DELTA_LIST = [1, 0, -1, 0]
    Y_DELTA_LIST = [0, 1, 0, -1]
    # Penalidad por pasar por un obstaculo, da mayor prefencia a soluciones sin obtáculos
    OBSTACLE_PENALTY = 1000

    def __init__(self, maze=None):
        self.chromosomes = []
        self.fitness = 99999
        if maze:
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

                fitness += 1
                if position != FINISH_POINT:
                    fitness += position * self.OBSTACLE_PENALTY
                # actualizo la posicion actual
                self.position_x += dx
                self.position_y += dy
                # agrego los datos del cromosoma
                self.chromosomes.append(Chromosome(self.position_x, self.position_y, step))
            except IndexError as error:
                position = 0
        self.fitness = fitness

    # Print the solution in screen
    def print_solution(self):
        # TODO: imprimir matriz resuelta
        print "Fitness: %d" % self.fitness
        print "Camino mínimo: " + ", ".join([str(chrom.position) for chrom in self.chromosomes])
        print "Direcciones: " + ", ".join([str(chrom.step) for chrom in self.chromosomes])

    def update_fitness(self, value=None):
        if value:
            self.fitness = value
        else:
            fitness = 0
            for chrom in self.chromosomes[:-1]:
                fitness += self.matrix[chrom.x][chrom.y]
            fitness *= self.OBSTACLE_PENALTY
            fitness += len(self.chromosomes)
            self.fitness = fitness

    def eliminate_loops(self):
        index = None
        loop_found = True
        new_chromosomes_list = list(self.chromosomes)
        while loop_found:
            index = 0
            while index < len(new_chromosomes_list):
                try:
                    loop_index = new_chromosomes_list.index(new_chromosomes_list[index], index + 1)
                except ValueError:
                    loop_found = False
                    index += 1
                else:
                    loop_found = True
                    new_chromosomes_list = new_chromosomes_list[:index+1] + new_chromosomes_list[loop_index+1:]
                    break
            if index >= len(new_chromosomes_list):
                loop_found = False
        self.chromosomes = new_chromosomes_list
        self.update_fitness()

    def mate(self, another_solution):
        found = False
        children = []
        found = False
        for index in range(len(self.chromosomes)):
            try:
                mate_index = another_solution.chromosomes.index(self.chromosomes[index])
            except ValueError:
                pass
            else:
                # print "PADRE"
                # self.print_solution()
                # print "OTRO PADRE"
                # another_solution.print_solution()
                found = True
                break
        if found:
            a_new_solution = Solution()
            a_new_solution.chromosomes = self.chromosomes[:index] + another_solution.chromosomes[mate_index:]
            a_new_solution.fitness = 99999
            a_new_solution.position_x = self.position_x
            a_new_solution.position_y = self.position_y
            a_new_solution.matrix = self.matrix
            a_new_solution.update_fitness()
            # print "Un HIJO"
            # a_new_solution.print_solution()
            children.append(a_new_solution)
            a_new_solution = Solution()
            a_new_solution.chromosomes = another_solution.chromosomes[:mate_index] + self.chromosomes[index:]
            a_new_solution.fitness = 99999
            a_new_solution.position_x = self.position_x
            a_new_solution.position_y = self.position_y
            a_new_solution.matrix = self.matrix
            a_new_solution.update_fitness()
            # print "Otro HIJO"
            # a_new_solution.print_solution()
            children.append(a_new_solution)
        return children


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
        # TODO: Lo pongo para hacer pruebas
        self.best_posible = 20

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
        self.matrix[6][3] = 7
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
            a_solution.eliminate_loops()
            # a_solution.print_solution()
            self.population.append(a_solution)

    # Evaluates if we arrived to a good solution
    def has_finished(self):
        if self.iteration >= self.max_iteration:
            self.finish = True
        # TODO: Dar un valor a self.best_posible
        elif self.population[0].fitness <= self.best_posible:
            self.finish = True
        return self.finish

    # Order the list by fitness
    def calc_fitness(self):
        self.population.sort(key=lambda solution: solution.fitness)

    # Mutates the solutions according to the parameters passed on the init
    def mutate(self):
        pass

    # Mates the solutions according to the  parameters passed on the initialization
    def mate(self):
        mating_subjects = self.population[:5]
        for i in range(len(mating_subjects)):
            a_subject = self.population[i]
            for j in range(5-i-1):
                another_subject = self.population[i + j + 1]
                children = a_subject.mate(another_subject)
                self.population.extend(children)

    # Return the solution with best fitness score
    def get_winner(self):
        return self.population[0]

    def select(self):
        self.population = self.population[:40]


def main():
    # TODO: pasar parámetros al constructor
    maze = Maze(500, 1000)
    maze.load_map()
    maze.init_population()
    maze.calc_fitness()
    maze.select()
    while not maze.has_finished():
        maze.mate()
        maze.mutate()
        maze.calc_fitness()
        maze.select()
        maze.iteration += 1
    winner = maze.get_winner()
    print maze.matrix
    winner.print_solution()


if __name__ == '__main__':
    main()
