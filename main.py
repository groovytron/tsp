from city import City, Link

if __name__ == "__main__":
    # dictionnaire contenant les villes
    # clé: nom de la ville, valeur: objet City
    cities = {}

    with open('data/pb005.txt', encoding='utf-8') as positions_file:
        for line in positions_file:
            # pour chaque ligne, on crée une ville avec les coordonnées associées
            cityname, x, y = line.split()
            cities[cityname] = City(cityname, (int(x), int(y)))
        print(cities)