import random

from solution import Solution
from travel import City
from gui import Gui

def main():
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


if __name__ == "__main__":
    main()