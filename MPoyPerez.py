"""
Script solving the famous Travel Salesman Problem (aka TSP).

Script can be given the following parameters:
    * --nogui: disables graphic user interface display.
    * --maxtime N: specifies maximum time in seconds for the script to look for
        a solution.
    * --filename FILE: uses the file given as input to set the cities list.
    * --maxstagnation N: specifies the number of iterations with stagnation
        before stopping the algorithm.

Authors: M'Poy Julien & Perez Joaquim
Date: 15.01.2017
Location: Haute École Arc, Neuchâtel
"""
from math import ceil
from itertools import chain
import time
import copy
import random
import pygame
import sys
from operator import attrgetter
from functools import total_ordering
from pygame.locals import (
    KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE,
    K_SPACE
)


"""
City class
"""


class City:
    """Class representing a city."""

    def __init__(self, name, position):
        """Name is city's name and position is a two floats tuple."""
        self.name = name
        self.position = position

        # will contain the next city and the distance to it
        # when creating a solution
        self.next = None
        self.dist = None

    def __eq__(self, other):
        try:
            return self.name == other.name and self.position == other.position
        except AttributeError:
            return False

    def __repr__(self):
        return "{} {}\n".format(self.name, self.position)

    def __hash__(self):
        return hash(self.name)

    def get_closest(self, cities):
        closest = cities[0]
        closest_dist = self.distance_to(closest)
        for city in cities:
            if self.distance_to(city) < closest_dist:
                closest = city
        return closest

    def distance_to(self, other):
        dx, dy = (
            self.position[0] - other.position[0],
            self.position[1] - other.position[1]
        )
        return (dx*dx + dy*dy) ** .5

"""
Solution
"""


@total_ordering
class Solution:
    def __init__(self, cities):
        """
        cities is an ordered list of cities, the last one is linked to the
        first one
        """
        self.cities = copy.copy(cities)
        self.compute_fitness()

    def compute_fitness(self):
        self.fitness = 0
        self.dict = {}

        old_city = self.cities[0]
        for city in chain(self.cities + [old_city]):
            distance = old_city.distance_to(city)
            # add the distance between this city and
            # the previous one to the fitness
            self.fitness += distance
            old_city.next = city
            old_city.dist = distance
            self.dict[old_city.name] = old_city
            old_city = city

    # total_ordering makes solutions comparable from these 2 methods
    def __eq__(self, other):
        return self.fitness == other.fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __repr__(self):
        return "solution with fitness {}".format(self.fitness)

    def mutate(self):
        """
        two blocks inversion (not indispensable)
        ABCDEF becomes CDEFAB

        The solution keeps the same, it only gives more chances to the FA
        segment to be muted.
        """
        pivot = random.randrange(len(self.cities))
        self.cities = self.cities[pivot:] + self.cities[:pivot]

        # i <- minimum born, j <- maximum born
        i = random.randrange(len(self.cities)-1)
        j = random.randrange(i+1, len(self.cities))

        # C
        # D
        # E <-- i
        # F
        # A <-- j
        # B

        top = self.cities[:i]  # CD
        middle = self.cities[i:j]  # EF
        bottom = self.cities[j:]  # AB
        # tidying block
        self.cities = middle + top + bottom  # EFCDAB

        self.compute_fitness()

    @staticmethod
    def create_pseudo_best(cities):
        # petite copie oklm pour ne pas toucher aux objets originaux
        cities = list(cities)
        ordered_cities = []
        city = cities[0]
        ordered_cities.append(city)
        cities.remove(city)
        while cities:
            city = city.get_closest(cities)
            ordered_cities.append(city)
            cities.remove(city)
        return Solution(ordered_cities)

"""
GUI
"""


class Gui:
    """Gui screen using pygame."""
    def __init__(self, cities=None, file_name=''):
        self.screen_x = 500
        self.screen_y = 500
        self.city_color = [10, 10, 200]  # blue
        self.city_radius = 3
        self.font_color = [255, 255, 255]  # white
        pygame.init()
        self.window = pygame.display.set_mode((self.screen_x, self.screen_y))
        pygame.display.set_caption('Travelling Salesman Problem')
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)

        if cities:
            self.cities = cities
            self.draw_cities()
            self.text(file_name)
            pygame.display.flip()
            self.wait_for_user_input()
        else:
            self.cities = []
            self.place_cities()

    def wait_for_user_input(self):
        while True:
            event = pygame.event.wait()
            if (event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE
            )):
                sys.exit(0)
            elif (event.type == KEYDOWN and (
                    event.key == K_RETURN or event.key == K_SPACE
                )
            ):
                break

    def place_cities(self):
        city_counter = 0
        self.screen.fill(0)
        self.text("Placez vos point puis appuyez sur Enter")
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    name = "v{}".format(city_counter)
                    self.cities.append(City(name, pos))
                    city_counter += + 1
                    self.screen.fill(0)
                    self.draw_cities()
                    self.text("Nombre: {}".format(len(self.cities)))
                    pygame.display.flip()
                elif (event.type == QUIT or (
                        event.type == KEYDOWN and event.key == K_ESCAPE
                    )
                ):
                    sys.exit(0)
                elif (event.type == KEYDOWN and (
                    event.key == K_RETURN or event.key == K_SPACE
                    )
                ):
                    if(len(self.cities) > 2):
                        return

    def draw_cities(self):
        for city in self.cities:
            pygame.draw.circle(
                self.screen, self.city_color, city.position, self.city_radius
            )

    def draw_path(self, solution, msg="", color=[255, 0, 0]):
        self.screen.fill(0)
        pygame.draw.lines(self.screen, color, True, [
            city.position for city in solution.cities]
        )
        self.draw_cities()
        self.text(msg)
        pygame.display.flip()

    def text(self, msg, render=False):
        text = self.font.render(msg, True, self.font_color)
        textRect = text.get_rect()
        self.screen.blit(text, textRect)
        if render:
            pygame.display.flip()

"""
Algorithme
"""


def crossover_from_best_in_parents(father, mother):
    """
    Starting from a city randomly selected, we check both parents'
    nex city and choose the closest one. If this city is already present
    in the solution, we take the other parent's one. If this city is
    already in the solution too, we choose an other city randomly.
    """
    children = []
    for i in range(2):
        cities = []
        names = [city.name for city in father.cities]
        chosen_name = random.choice(names)
        while len(names) > 0:
            names.remove(chosen_name)
            current_city = father.dict[chosen_name]
            cities.append(current_city)
            from_father = father.dict[chosen_name]
            from_mother = mother.dict[chosen_name]

            candidates = []
            if from_father.next.name in names:
                candidates += [from_father]
            if from_mother.next.name in names:
                candidates += [from_mother]

            if len(candidates) > 0:
                # we can use a gene from one the parents
                candidates.sort(key=attrgetter('dist'))
                chosen_name = candidates[0].next.name
            else:
                """
                we cannot because both cities are already in the solution
                we are building.
                """
                if names:
                    chosen_name = random.choice(names)
        children += [Solution(cities)]

    return children


def ox_crossover(x, y, crossover_ratio=0.3):
    """
    OX Crossover between x and y indviduals. Crossover section is defined
    randomly following the crossover_ration parameter.

    The two children are generated and returned as a tuple containing.
    """
    x, y = x.cities, y.cities
    genes_to_crossover = int(ceil(len(x) * crossover_ratio))
    start = random.randint(0, len(x) - genes_to_crossover - 1)
    stop = start + genes_to_crossover
    x_crossover = tuple(x[start:stop])
    y_crossover = tuple(y[start:stop])
    prepared_x = [item if item not in y_crossover else None for item in x]
    x_shifts = prepared_x[stop:].count(None)
    prepared_y = [item if item not in x_crossover else None for item in y]
    y_shifts = prepared_y[stop:].count(None)
    new_x = [item for item in prepared_x if item is not None]
    new_y = [item for item in prepared_y if item is not None]
    new_x = shift_list(new_x, x_shifts)
    new_y = shift_list(new_y, y_shifts)
    new_x = new_x[:start] + list(y_crossover) + new_x[start:]
    new_y = new_y[:start] + list(x_crossover) + new_y[start:]
    return Solution(new_x), Solution(new_y)


def shift_list(items, shifts):
    """Left shift a list of elements."""
    for i in range(shifts):
        items = items[1:] + items[:1]
    return items


def ga_solve(file=None, gui=True, maxtime=0, maxstagnation=200):
    """
    Main function parsing file, initializing UI and launching genetic
    algorithm solving method.
    """

    # dictionnary containing the cities
    # key: city's name, value: City object
    cities = []

    # just because we are already using a gui variable
    gui_diplay = gui

    if file:
        with open(file, encoding='utf-8') as positions_file:
            for line in positions_file:
                # for each line, we create a City object with the coordinates
                cityname, x, y = line.split()
                cities.append(City(cityname, (int(x), int(y))))
            if gui_diplay:
                gui = Gui(cities, file)
    else:
        gui = Gui()
        cities = gui.cities

    t1 = time.time()

    POPULATION_SIZE = 20
    # int because division always returns a float
    HALF = int(POPULATION_SIZE/2)
    QUARTER = int(POPULATION_SIZE/4)
    # mutation rate
    rate = 0.2

    """
    RANGS contains n*0,  (n-1)*1 ... 1*n
        -> example 10, 9,9, 8,8,8, 7,7,7,7, ...
    """
    RANGS = [
        POPULATION_SIZE-i for i in range(POPULATION_SIZE+1) for j in range(i)
    ]

    population = []
    for i in range(POPULATION_SIZE):
        random.shuffle(cities)
        population.append(Solution(cities))

    pseudo_best = Solution.create_pseudo_best(cities)
    population.append(pseudo_best)

    old_best = 0
    stagnation = 0

    method_1 = True

    # genetic algorithm
    while True:
        # population sorting
        population.sort()

        best = Solution(population[0].cities)

        # population = population[:HALF] # selects half of the best solutions

        # more natural selection
        # select a quarter of the best solutions
        population = population[:QUARTER]
        # the select an other quarter randomly
        # population[QUARTER:] remains
        population += random.sample(population, QUARTER)

        # seems more correct but works gives worse results
        # elite, reste = population[:QUARTER], population[QUARTER:]
        # population = elite + random.sample(population, QUARTER)

        # population shuffling
        random.shuffle(population)

        # crossover
        for i in range(0, HALF, 2):  # 0 to HALF 2-by-2
            sol1 = population[i]
            sol2 = population[i+1]
            # add children to the population
            if method_1:
                population += crossover_from_best_in_parents(sol1, sol2)
            else:
                population += list(ox_crossover(sol1, sol2))
            method_1 = not method_1

        # muate 20% of the solutions
        [
            solution.mutate() for solution in random.sample(
                population, int(rate * len(population))
            )
        ]
        population.append(best)

        if best.fitness == old_best:
            stagnation += 1
            # stop if the best solution is the same n time consequently
            if not maxtime and stagnation == maxstagnation:
                break
        else:
            stagnation = 0
            if gui_diplay:
                gui.draw_path(best, msg=str(best.fitness))

        if maxtime:
            dt = time.time() - t1
            if dt > maxtime:
                break

        old_best = best.fitness

    if gui_diplay:
        gui.draw_path(best, msg=str(best.fitness), color=[0, 255, 0])
        gui.wait_for_user_input()

    path = [city.name for city in best.cities]
    return best.fitness, path

"""
MAIN
"""
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", help="use the file given as input")
    parser.add_argument(
        "-n", "--nogui",
        help="disable graphic user interface display", action="store_true"
    )
    parser.add_argument(
        "-t", "--maxtime", help="specify the maximum time in seconds", type=int
    )
    parser.add_argument(
        "-s", "--maxstagnation", type=int, default=200,
        help="specify the number of iteration with \
            stagnation before stopping the algorithm"
    )
    args = parser.parse_args()

    distance, path = ga_solve(
        file=args.filename,
        gui=not args.nogui,
        maxtime=args.maxtime,
        maxstagnation=args.maxstagnation
    )

    print("Distance : {}\nPath : {}".format(distance, path))
