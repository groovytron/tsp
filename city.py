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
