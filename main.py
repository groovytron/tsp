import random

from solution import Solution
from city import City
from gui import Gui
import time

def main():
    """
    Main function parsing file, initializing UI and launching genetic
    algorithm solving method.
    """
    # dictionnaire contenant les villes
    # clé: nom de la ville, valeur: objet City
    cities = {}

    file_name = 'data/pb050.txt'
    # file_name = ''

    if file_name:
        with open(file_name, encoding='utf-8') as positions_file:
            for line in positions_file:
                # pour chaque ligne, on crée une ville avec les coordonnées
                # associées
                cityname, x, y = line.split()
                cities[cityname] = City(cityname, (int(x), int(y)))
            gui = Gui(cities, file_name)
    else:
        gui = Gui()
        cities = gui.cities

    cities = list(cities.values())
    population = []

    max_time = 15
    POPULATION_SIZE = 100
    HALF = int(POPULATION_SIZE/2) # int car la division retourne un float dans tous les cas
    QUARTER = int(POPULATION_SIZE/4)
    # taux de mutation
    rate = 0.2

    RANGS = [POPULATION_SIZE-i for i in range(POPULATION_SIZE+1) for j in range(i)]
    # RANGS contient n*0,  (n-1)*1 ... 1*n -> exemple 10, 9,9, 8,8,8, 7,7,7,7, ...

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

    t1 = time.time()

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
            if not max_time and stagnation == 100:
                break
        else:
            stagnation = 0
            gui.draw_path(best, msg=str(best.fitness))

        if max_time:
            dt = time.time() - t1
            if dt > max_time: break

        old_best = best.fitness

    gui.draw_path(best, msg=str(best.fitness), color=[0,255,0])
    gui.wait_for_user_input()


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


if __name__ == "__main__":
    main()
