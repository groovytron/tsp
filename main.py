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

    file_name = 'data/pb005.txt'
    # file_name = ''

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
    for i in range(100):
        random.shuffle(cities)
        population.append(Solution(cities))

    population.sort()

    bad = population[-1].cities
    better = population[0].cities

    # Population selection
    selected_population = [
        random.choice(population) for i in range(int(len(population) / 2) - 1)
    ]
    selected_population.append(better)

    # Crossover tests
    print('crossover between bad and better')
    child1, child2 = crossover(bad, better)
    print('child 1', child1)
    print('child 2', child2)
    print('Resulting new population adaptaility comparison')
    print('better', Solution(better))
    print('bad', Solution(bad))
    print('child 1', Solution(child1))
    print('child 2', Solution(child2))

    gui.draw_path(
       [city.position for city in bad], msg="bad solution", color=[255, 0, 0]
    )
    gui.wait_for_user_input()

    gui.draw_path([city.position for city in better], msg="better solution")
    gui.wait_for_user_input()


def crossover(x, y, start=2, stop=4):
    """
    Crossover x and y indviduals' genes at indices between start and stop.

    The two children are generated and returned as a tuple containing.
    """
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
    return new_x, new_y


def shift_list(items, shifts):
    """Left shift a list of elements."""
    for i in range(shifts):
        items = items[1:] + items[:1]
    return items


if __name__ == "__main__":
    main()
