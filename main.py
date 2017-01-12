import random

from solution import Solution
from city import City
from gui import Gui


def main():
    """
    Main function parsing file, initializing UI and launching genetic
    algorithm solving method.
    """
    # dictionnaire contenant les villes
    # clé: nom de la ville, valeur: objet City
    cities = {}

    # file_name = 'data/pb005.txt'
    file_name = ''

    if file_name:
        with open(file_name, encoding='utf-8') as positions_file:
            for line in positions_file:
                # pour chaque ligne, on crée une ville avec les coordonnées
                # associées
                cityname, x, y = line.split()
                cities[cityname] = City(cityname, (int(x), int(y)))
            gui = Gui(cities)
    else:
        gui = Gui()
        cities = gui.cities

    cities = list(cities.values())
    population = []

    POPULATION_SIZE = 12
    HALF = int(POPULATION_SIZE/2) # int car la division retourne un float dans tous les cas

    for i in range(POPULATION_SIZE):
        random.shuffle(cities)
        population.append(Solution(cities))

    population.sort()

    old_best = population[0]
    gui.draw_path([city.position for city in old_best.cities])
    stagnation = 0


    # algo génétique
    while True:
        # trier la population
        population.sort()

        best = population[0]

        # selection : enlever la moitié
        # todo: selection par roulette ou par rang
        population = population[:HALF] # sélectionne la moitié meilleure

        # mélange la population
        random.shuffle(population)

        # croisement
        for i in range(0, HALF, 2): # 0 to HALF 2-by-2
            sol1 = population[i]
            sol2 = population[i+1]
            # ajoute les enfants à la population
            population += sol1.crossing(sol2)
            population += list(crossover(sol1, sol2))

        # muter 20% des solutions
        [solution.mutate() for solution in random.sample(population, int(0.2*len(population)))]

        # temporaire : remplissage avec des solutions random
        while len(population) < POPULATION_SIZE:
            random.shuffle(cities)
            population.append(Solution(cities))

        # sortir si la meilleure solution est la même n fois de suite
        if best == old_best:
            stagnation += 1
            if stagnation == 500:
                break
        else:
            stagnation = 0
            gui.draw_path([city.position for city in best.cities], msg=str(best.fitness))

        old_best = best

    gui.draw_path([city.position for city in best.cities], msg="voilà")

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
