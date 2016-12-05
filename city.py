
class Link:
	def __init__(self, city1, city2, distance):
		self.cities = (city1,city2)
		self.distance = distance
		
	def __repr__(self):
		return "({}-{}:{})".format(self.cities[0].name, self.cities[1].name, self.distance)
		
	def get_other(self, city1):
		'''reçoit une des extrémités du lien et retourne l'autre'''
		if city1 == self.cities[0]: return self.cities[1]
		else: return self.cities[0]

class City:
	def __init__(self, name, position):
		self.name=name
		self.links=[]
		# tuple (x,y)
		self.position=position
	
	def add_link(self, link):
		self.links.append(link)
		
	def __repr__(self):
		str = "{} {}\n".format(self.name, self.position)
		for link in self.links:
			str += " -> {}\n".format(link)
		return str