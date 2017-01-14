import copy, random
from operator import attrgetter
from functools import total_ordering

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
        ordered_cities = []
        city = cities[0]
        ordered_cities.append(city)
        cities.remove(city)
        while cities:
            city = city.get_closest(cities)
            ordered_cities.append(city)
            cities.remove(city)
        return Solution(ordered_cities)