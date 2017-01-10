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
    for i in range(10):
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

        # sortir la meilleure solution
        best = population.pop(0)

        # selectionner qlqs couples
        couples = []
        for i in range(2):
            # todo: selection par roulette ou par rang
            couples.append((population.pop(0), population.pop(0)))

        # croisement des paires
        children = []
        for sol1, sol2 in couples:
            children += sol1.crossing(sol2)

        # remplacer une partie de la population par les enfants obtenus
        population = [best] + children

        # temporaire : remplissage avec des solutions random
        while len(population) < 10:
            random.shuffle(cities)
            population.append(Solution(cities))

        # muter qlqs solutions

        # sortir si la meilleure solution est la même n fois de suite
        if best is old_best:
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