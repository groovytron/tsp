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
    for i in range(5):
        random.shuffle(cities)
        population.append(Solution(cities))

    population.sort()

    bad = population[-1].cities
    better = population[0].cities

    gui.draw_path([city.position for city in bad], msg="bad solution", color=[255,0,0])
    gui.wait_for_user_input()

    gui.draw_path([city.position for city in better], msg="better solution")
    gui.wait_for_user_input()


if __name__ == "__main__":
    main()