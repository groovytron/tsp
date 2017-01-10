import copy

class Solution:
    def __init__(self, cities):
        # cities is an ordered list of cities, the last one is linked to the first one
        self.cities = copy.deepcopy(cities)
        self.compute_fitness()

    def compute_fitness(self):
        self.fitness = 0

        def dist(pos1, pos2):
            dx, dy = abs(old_pos[0] - new_pos[0]), abs(old_pos[1] - new_pos[1])
            return (dx*dx + dy*dy) ** .5

        old_pos = self.cities[0].position
        for city in self.cities:
            new_pos = city.position
            # add to the fitness the distance between this city and the previous one
            self.fitness += dist(old_pos, new_pos)
            old_pos = new_pos

        # compute distance from the last city to the first
        new_pos = self.cities[0].position
        self.fitness += dist(old_pos, new_pos)

    # these 2 methods makes solutions comparable
    def __eq__(self, other):
        return self.fitness == other.fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __repr__(self):
        return "solution with fitness {}".format(self.fitness)

    def crossing(self, other):
        children = []
        # todo
        return children

    def mutate(self):
        pass