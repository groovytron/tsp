import random

from solution import Solution
from travel import City
from gui import Gui

def get_cities():
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
    return cities


if __name__ == "__main__":
    cities = list(get_cities().values())
    population = []
    for i in range(10):
        copy = cities
        random.shuffle(copy)
        population.append(Solution(copy))
        print(population[-1])
    population.sort()
    print("best solution :", population[0])
    print("worst solution :", population[-1])