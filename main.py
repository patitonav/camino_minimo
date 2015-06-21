#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

import numpy  # sudo apt-get install python-numpy
import random
import pdb
import timeit
from unicodedata import *

# Matrix
# -------
# 9: Wall
# 8: Starting Point
# 7: Finish Point
# (1-6): Different obstacles
# 0: Walkable
FINISH_POINT = 7
STARTING_POINT = 8
MUTATION_NUMBER = 15


class Chromosome():

    def __init__(self, x, y, step, cost):
        self.x = x
        self.y = y
        self.step = step
        self.cost = cost

    @property
    def position(self):
        return self.x, self.y

    def get_cost(self):
        if self.cost == FINISH_POINT:
            return 0
        return self.cost

    def __eq__(self, other):
        if isinstance(other, Chromosome):
            return self.position == other.position
        else:
            return NotImplemented

    def __repr__(self):
        return "(%d,%d), paso:%d, costo:%d" % (self.x, self.y, self.step, self.get_cost())


class Solution:

    X_DELTA_LIST = [1, 0, -1, 0]
    Y_DELTA_LIST = [0, 1, 0, -1]
    # Penalidad por pasar por un obstaculo, da mayor prefencia a soluciones sin obtáculos
    OBSTACLE_PENALTY = 1000

    def __init__(self, maze=None):
        self.chromosomes = []
        self.fitness = 99999
        if maze:
            self.position_x = maze.initial_position_x
            self.position_y = maze.initial_position_y
            self.matrix = maze.matrix

    def get_chromosomes(self):
        return self.chromosomes

    def set_chromosomes(self, new_chromosomes):
        self.chromosomes=new_chromosomes

    # Make a solution for the maze and get fitness and sets the fitness
    def run(self):
        position = 0
        fitness = 0
        while position != FINISH_POINT:
            step = random.randint(0, 3)  # 0: DOWN, 1: RIGHT, 2: UP, 3: LEFT
            dx = self.X_DELTA_LIST[step]
            dy = self.Y_DELTA_LIST[step]
            try:
                if self.position_x + dx > 0 and self.position_y + dy > 0:
                    position = self.matrix[self.position_x + dx][self.position_y + dy]
                    fitness += 1
                    if position != FINISH_POINT:
                        fitness += position * self.OBSTACLE_PENALTY
                    # actualizo la posicion actual
                    self.position_x += dx
                    self.position_y += dy
                    # agrego los datos del cromosoma
                    self.chromosomes.append(Chromosome(self.position_x, self.position_y, step,self.matrix[self.position_x,self.position_y]))
            except IndexError as error:
                position = 0
        self.fitness = fitness



    def print_directions(self,string_directions):
        string_directions=string_directions.replace("0", u"↓");
        string_directions=string_directions.replace("1", u"→");
        string_directions=string_directions.replace("2", u"↑");
        string_directions=string_directions.replace("3", u"←");
        return string_directions


    # Print the solution in screen
    def print_solution(self):
        # TODO: imprimir matriz resuelta
        print "Fitness: %d" % self.fitness
        print "Camino mínimo: " + ", ".join([str(chrom.position) for chrom in self.chromosomes])
        print "Direcciones: " + self.print_directions(", ".join([str(chrom.step) for chrom in self.chromosomes]))

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

    def split_chromosomes(self):
        a_solution=self.get_chromosomes()
        length = len(a_solution)
        return [ a_solution[i*length // MUTATION_NUMBER: (i+1)*length // MUTATION_NUMBER] for i in range(MUTATION_NUMBER) ]

    def join_chromosomes(self, a_list_of_grouped_chromosomes):
        return [j for i in a_list_of_grouped_chromosomes for j in i]
    

    # Mutates the solutions according to the parameters passed on the init
    def mutate(self):
        try:
            splitted_solution=self.split_chromosomes()
            max_fitness=0
            unfit_block_of_chromosomes=[]
            index_in_splitted_solution=0
            for i, block_of_chromosomes in enumerate(splitted_solution):
                a_fitness=0
                for chromosome in block_of_chromosomes:
                    a_fitness+=chromosome.get_cost()
                if a_fitness > max_fitness:
                    max_fitness=a_fitness
                    unfit_block_of_chromosomes=block_of_chromosomes
                    index_in_splitted_solution=i

            mutated_block_of_chromosomes=[]
            # print index_in_splitted_solution
            if index_in_splitted_solution != 0:
                last_position_x = splitted_solution[index_in_splitted_solution - 1][-1].x
                last_position_y = splitted_solution[index_in_splitted_solution - 1][-1].y
            else:
                first_chromosome = splitted_solution[0][0]
                # Cargo el primer cromosoma
                mutated_block_of_chromosomes.append(first_chromosome)
                # Su posicion es la ultima visitada
                last_position_x = first_chromosome.x
                last_position_y = first_chromosome.y
            #splitted_solution[index_in_splitted_solution-1][-1] indica el ultimo cromosoma del ultimo cacho antes del que hay que mudar

            if splitted_solution[index_in_splitted_solution]==splitted_solution[-1]: #si el bloque a mutar es el último
                finishing_point = FINISH_POINT
                finishing_x = splitted_solution[index_in_splitted_solution][-1].x
                finishing_y = splitted_solution[index_in_splitted_solution][-1].y
            else:
#                try:
                finishing_point = self.matrix[splitted_solution[index_in_splitted_solution+1][0].x][splitted_solution[index_in_splitted_solution+1][0].y]
                finishing_x = splitted_solution[index_in_splitted_solution+1][0].x
                finishing_y = splitted_solution[index_in_splitted_solution+1][0].y

 #               except Exception as error:
 #                   print error
 #                   pdb.set_trace()
                #si no es el ultimo, se toma como finishing point el primero del siguiente

            position = 0
            fitness = 0

            while finishing_x != last_position_x or finishing_y != last_position_y:
                step = random.randint(0, 3)  # 0: DOWN, 1: RIGHT, 2: UP, 3: LEFT
                dx = self.X_DELTA_LIST[step]
                dy = self.Y_DELTA_LIST[step]
                try:
                    if last_position_x + dx > 0 and last_position_y + dy > 0:
                        position = self.matrix[last_position_x + dx][last_position_y + dy]
                        fitness += 1
                        if position != finishing_point:
                            fitness += position * self.OBSTACLE_PENALTY
                        # actualizo la posicion actual
                        last_position_x += dx
                        last_position_y += dy
                        ###########
                        mutated_block_of_chromosomes.append(Chromosome(last_position_x, last_position_y, step,self.matrix[last_position_x,last_position_y]))
                except IndexError as error:
                    position = 0
         #-------------
            #reemplazo y unifico
            splitted_solution[index_in_splitted_solution]=mutated_block_of_chromosomes
            self.set_chromosomes(self.join_chromosomes(splitted_solution)) #transformo todo en una sola lista de nuevo.
            self.eliminate_loops()
            self.update_fitness()
        except Exception as error:
#            print error
             pass


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
        self.initial_position_x = None
        self.initial_position_y = None
        # TODO: Lo pongo para hacer pruebas
        self.best_posible = 9

    def set_stating_point(self):

        x = 0
        for row in self.matrix:
            y = 0
            for col in row:
                if col == STARTING_POINT:
                    self.initial_position_x = x
                    self.initial_position_y = y
                    break
                y += 1
            if self.initial_position_x and self.initial_position_y:
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
        self.matrix[1][6] = 8
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

    def mutate(self):
        for a_solution in self.population:
            a_solution.mutate()

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
        TOP = 20
        index = random.randint(TOP, len(self.population) - 1)
        self.population = self.population[:TOP] + self.population[index:TOP + index]


def main():
    # TODO: pasar parámetros al constructor
    maze = Maze(1000, 50)
    maze.load_map()
    maze.init_population()
    maze.calc_fitness()
    maze.select()
    clock_start = timeit.default_timer()
    while not maze.has_finished():
        maze.mate()
        maze.mutate()
        maze.calc_fitness()
        maze.select()
        maze.iteration += 1
    winner = maze.get_winner()
    clock_stop = timeit.default_timer()
    #print maze.matrix
    winner.print_solution()
    print "Tiempo tomado por alg. genético: " + str(clock_stop - clock_start) + " segundos"



if __name__ == '__main__':
    random.seed()
    main()
