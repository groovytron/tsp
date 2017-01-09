class Solution:
    def __init__(self, cities):
        # cities is an ordered list of cities, the last one is linked to the first one
        self.cities = cities
        self.fitness = 0

        # compute fitness
        old_pos = cities[0].position
        for city in cities:
            new_pos = city.position
            # dx, dy = abs(old_pos - new_pos)
            dx, dy = abs(old_pos[0] - new_pos[0]), abs(old_pos[1] - new_pos[1])
            # add to the fitness the distance between this city and the previous one
            self.fitness += (dx*dx + dy*dy) ** .5
            old_pos = new_pos

        # compute distance from the last city to the first
        # old_pos contains position of the last city in the list
        new_pos = cities[0].position
        # warning : repeated code (maybe lambda ?)
        dx, dy = abs(old_pos[0] - new_pos[0]), abs(old_pos[1] - new_pos[1])
        self.fitness += (dx*dx + dy*dy) ** .5

    # these 2 methods makes solutions comparable
    def __eq__(self, other):
        return self.fitness == other.fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __repr__(self):
        return "solution with fitness {}".format(self.fitness)