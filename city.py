class City:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    # these 2 methods makes solutions comparable
    def __eq__(self, other):
        try:
            return self.name == other.name and self.position == other.position
        except AttributeError:
            return False

    def __repr__(self):
        str = "{} {}\n".format(self.name, self.position)
        return str
