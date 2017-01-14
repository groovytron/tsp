class City:
    """Class representing a city."""

    def __init__(self, name, position):
        """Name is city's name and position is a two floats tuple."""
        self.name = name
        self.position = position

        # will contain the next city and the distance to it
        # when creating a solution
        self.next = None
        self.dist = None

    def __eq__(self, other):
        try:
            return self.name == other.name and self.position == other.position
        except AttributeError:
            return False

    def __repr__(self):
        return "{} {}\n".format(self.name, self.position)

    def __hash__(self):
        return hash(self.name)

    def get_closest(self, cities):
        closest = cities[0]
        closest_dist = self.distance_to(closest)
        for city in cities:
            if self.distance_to(city) < closest_dist:
                closest = city
        return closest

    def distance_to(self, other):
        dx, dy = self.position[0] - other.position[0], self.position[1] - other.position[1]
        return (dx*dx + dy*dy) ** .5
