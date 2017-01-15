###
### imports
###

import time, copy, random, pygame, sys
from operator import attrgetter
from functools import total_ordering
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE, K_SPACE

###
### CITY
###

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
        dx, dy = self.position[0] - other.position[0], self.position[1] - other.position[1]
        return (dx*dx + dy*dy) ** .5

###
### SOLUTION
###

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
        for city in self.cities + [old_city]:
            distance = old_city.distance_to(city)
            # add to the fitness the distance between this city and the previous one
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

    def crossing(self, mother):
        """
        En partant d’une ville au hasard, considérer la ville suivante dans chacun des
        parents et choisir la plus proche. Si celle-ci est déjà présente dans la solution, prendre
        l’autre. Si elle est aussi déjà présente, choisir une ville non présente au hasard.
        """
        children = []
        for i in range(2):
            father = self
            cities = []
            names = [city.name for city in self.cities]
            chosen_name = random.choice(names)
            while len(names) > 0:
                names.remove(chosen_name)
                current_city = self.dict[chosen_name]
                cities.append(current_city)
                from_father = father.dict[chosen_name]
                from_mother = mother.dict[chosen_name]

                candidates = []
                if from_father.next.name in names:
                    candidates += [from_father]
                if from_mother.next.name in names:
                    candidates += [from_mother]

                if len(candidates) > 0:
                    # on peut utlisier un gene de l'un des parents
                    candidates.sort(key=attrgetter('dist'))
                    chosen_name = candidates[0].next.name
                else:
                    # on ne peut pas car 2 villes-next sont deja utilisées dans la nouvelle solution
                    if names:
                        chosen_name = random.choice(names)
            children += [Solution(cities)]

        return children

    def mutate(self):
        # inverse deux blocs (pas indispensable)
        # ABCDEF devient
        # CDEFAB
        # la solution reste la même, ça permet juste de donner des chances au segment FA d'être muté
        pivot = random.randrange(len(self.cities))
        self.cities = self.cities[pivot:] + self.cities[:pivot]

        # i <- borne inférieure, j <- borne supérieure
        i = random.randrange(len(self.cities)-1)
        j = random.randrange(i+1, len(self.cities))

        # C
        # D
        # E <-- i
        # F
        # A <-- j
        # B

        top = self.cities[:i] # CD
        middle = self.cities[i:j] # EF
        bottom = self.cities[j:] # AB
        # reordonne les blocs
        self.cities = middle + top + bottom # EFCDAB

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

###
### GUI
###

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
            if (event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE)):
                sys.exit(0)
            elif event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_SPACE):
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
                elif (event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE)):
                    sys.exit(0)
                elif event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_SPACE):
                    if(len(self.cities) > 2):
                        return

    def draw_cities(self):
        for city in self.cities:
            pygame.draw.circle(
                self.screen, self.city_color, city.position, self.city_radius
            )


    def draw_path(self, solution, msg="" , color=[255,0,0]):
        self.screen.fill(0)
        pygame.draw.lines(self.screen, color, True, [city.position for city in solution.cities])
        self.draw_cities()
        self.text(msg)
        pygame.display.flip()

    def text(self, msg, render=False):
        text = self.font.render(msg, True, self.font_color)
        textRect = text.get_rect()
        self.screen.blit(text, textRect)
        if render: pygame.display.flip()

###
### ALGORITHM
###

def crossover(x, y, start=2, stop=4):
    """
    Crossover x and y indviduals' genes at indices between start and stop.

    The two children are generated and returned as a tuple containing.
    """
    x,y = x.cities, y.cities
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

    cities = []

    # juste parce qu'on utilise deja une variable gui
    gui_diplay = gui

    if file:
        with open(file, encoding='utf-8') as positions_file:
            for line in positions_file:
                # pour chaque ligne, on crée une ville avec les coordonnées
                # associées
                cityname, x, y = line.split()
                cities.append(City(cityname, (int(x), int(y))))
            if gui_diplay:
                gui = Gui(cities, file)
    else:
        gui = Gui()
        cities = gui.cities

    # cities = list(cities)

    t1 = time.time()

    POPULATION_SIZE = 100
    HALF = int(POPULATION_SIZE/2) # int car la division retourne un float dans tous les cas
    QUARTER = int(POPULATION_SIZE/4)
    # taux de mutation
    rate = 0.2

    RANGS = [POPULATION_SIZE-i for i in range(POPULATION_SIZE+1) for j in range(i)]
    # RANGS contient n*0,  (n-1)*1 ... 1*n -> exemple 10, 9,9, 8,8,8, 7,7,7,7, ...

    population = []
    for i in range(POPULATION_SIZE):
        random.shuffle(cities)
        population.append(Solution(cities))

    pseudo_best = Solution.create_pseudo_best(cities)
    # gui.draw_path(pseudo_best, msg="pseudo best with fitness:{}".format(pseudo_best.fitness), color=[255,255,0])
    # gui.wait_for_user_input()
    population.append(pseudo_best)

    old_best=0
    stagnation = 0

    method_1 = True

    # algo génétique
    while True:
        # trier la population
        population.sort()

        best = Solution(population[0].cities)

        # population = population[:HALF] # sélectionne la moitié meilleure

        # selection un peu plus naturelle
        # selectionne un quart d'élite
        population = population[:QUARTER]
        # puis sélectionne un autre quart au pif
        # reste = population[QUARTER:]
        population += random.sample(population, QUARTER)

        # # plus juste mais marche moins bien
        # elite, reste = population[:QUARTER], population[QUARTER:]
        # population = elite + random.sample(population, QUARTER)

        # mélange la population
        random.shuffle(population)

        # croisement
        for i in range(0, HALF, 2): # 0 to HALF 2-by-2
            sol1 = population[i]
            sol2 = population[i+1]
            # ajoute les enfants à la population
            if method_1:
                population += sol1.crossing(sol2)
            else:
                population += list(crossover(sol1, sol2))
            method_1 = not method_1

        # muter 20% des solutions
        [solution.mutate() for solution in random.sample(population, int(rate*len(population)))]
        population.append(best)

        if best.fitness == old_best:
            stagnation += 1
            # sortir si la meilleure solution est la même n fois de suite
            if not maxtime and stagnation == maxstagnation:
                break
        else:
            stagnation = 0
            if gui_diplay:
                gui.draw_path(best, msg=str(best.fitness))

        if maxtime:
            dt = time.time() - t1
            if dt > maxtime: break

        old_best = best.fitness

    if gui_diplay:
        gui.draw_path(best, msg=str(best.fitness), color=[0,255,0])
        gui.wait_for_user_input()

    path = [city.name for city in best.cities]
    return best.fitness, path

###
### MAIN
###

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", help="use the file given as input")
    parser.add_argument("-n", "--nogui", help="disable graphic user interface display", action="store_true")
    parser.add_argument("-t", "--maxtime", help="specify the maximum time in seconds", type=int)
    parser.add_argument("-s", "--maxstagnation", type=int, default=200,
                        help="specify the number of iteration with stagnation before stopping the algorithm")
    args = parser.parse_args()

    distance, path = ga_solve(file=args.filename,
                              gui=not args.nogui,
                              maxtime=args.maxtime,
                              maxstagnation=args.maxstagnation)
    print("Distance : {}\nPath : {}".format(distance, path))

