#!/usr/bin/env python3
"""
Testeur systématique de solveur du problème du voyageur de commerce.

Permet de lancer automatiquement une série de solveurs sur une série de
problèmes et génère une grille de résultats au format CSV.

v0.2, Matthieu Amiguet, HE-Arc
v0.3, hatem Ghorbel, HE-Arc
v0.4, Romain Claret, HE-Arc
v0.5, Yoan Blanc, doSimple
"""

import csv
import multiprocessing
import os
import sys
from importlib import import_module
from itertools import cycle
from math import hypot, isclose

# PARAMETRES
# =========
# modifier cette partie pour l'adapter à vos besoins

# Le nom des modules à tester
# Ces modules doivent être dans le PYTHONPATH; p.ex. dans le répertoire courant

modules = (
    "MPoyPerez",
    # Éventuellement d'autres modules pour comparer plusieurs versions...
)

# Liste des tests à effectuer
# sous forme de couples (<datafile>, <maxtime>) où
# <datafile> est le fichier contenant les données du problème et
# <maxtime> le temps (en secondes) imparti pour la résolution
tests = (
    ('data/pb005.txt', 1),
    ('data/pb010.txt', 5),
    ('data/pb010.txt', 10),
    ('data/pb050.txt', 30),
    ('data/pb050.txt', 60),
    ('data/pb100.txt', 20),
    ('data/pb100.txt', 90), )

# On tolère un dépassement de 5% du temps imparti:
tolerance = 0.05

# Fichier dans lequel écrire les résultats
outfile = sys.stdout
# ou :
# outfile = 'results.csv'

# affichage à la console d'informations d'avancement?
verbose = False

# est-ce qu'on veut un affichage graphique?
gui = False

# PROGRAMME
# =========
# Cette partie n'a théoriquement pas à être modifiée


def dist(city1, city2):
    """Distance entre deux villes."""
    x1, y1 = city1
    x2, y2 = city2
    return hypot(x2 - x1, y2 - y1)


def validate(cities, length, path):
    """Validation de la solution."""
    try:
        c = cycle(path)
        next(c)
        totaldist = sum(
            dist(cities[src], cities[dst]) for src, dst in zip(path, c))

        if not isclose(totaldist, length):
            return False, "Wrong dist! (%.3f instead of %.3f)" % (length,
                                                                  totaldist)

    except KeyError as ke:
        return False, "City {0} does not exist!".format(*ke.args)
    except Exception as e:
        return False, "Error during validation: %r" % e

    missing_cities = set(cities.keys()) - set(path)
    if missing_cities:
        return False, "Not all cities visited! %r" % missing_cities

    return True, None


def main():
    """
    Programme principal.

    Récupération des différentes implémentations.

    On met les différentes fonctions ga_solve() dans un dictionnaire indexé par
    le nom du module correpsondant.

    On en profite pour écrire la ligne d'en-tête du fichier de sortie.
    """
    solvers = {}

    if isinstance(outfile, str):
        outf = open(outfile, 'w', newline='')
    else:
        outf = outfile
    out = csv.writer(outf, delimiter=';')

    row = ['Test']
    for m in modules:
        try:
            module = import_module(m)
            solvers[m] = module.ga_solve
            row.append(m)
        except Exception as e:
            row.append(str(e))

    out.writerow(row)

    # Cette partie effectue les tests proprement dits
    # et rapporte les résultats dans outfile

    with multiprocessing.Pool(processes=1) as pool:
        for filename, maxtime in tests:
            # Écriture de l'en-tête de ligne
            row = ["{0} ({1}s)".format(filename, maxtime)]

            with open(filename, newline='') as f:
                reader = csv.reader(f, delimiter=' ')
                cities = {name: (int(x), int(y)) for name, x, y in reader}

            if verbose:
                print("--> %s, %d" % (filename, maxtime), file=sys.stderr)

            # normalisation du nom de fichier (pour l'aspect multi-plateforme)
            filename = os.path.normcase(os.path.normpath(filename))

            # Appel des solveurs proprement dits, vérification et écriture des
            # résultats
            for m in modules:
                if verbose:
                    print("## %s" % m, file=sys.stderr)

                if m not in solvers:
                    row.append(-1)
                    continue

                try:
                    result = pool.apply_async(solvers[m],
                                              (filename, gui, maxtime))
                    try:
                        length, path = result.get(maxtime * (1 + tolerance))
                    except KeyboardInterrupt:
                        print("The pool is closing...", file=sys.stderr)
                        pool.terminate()
                        pool.join()
                except Exception as e:
                    row.append(e.__class__.__name__)
                else:
                    success, message = validate(cities, length, path)
                    if success:
                        row.append(int(length))
                    else:
                        row.append(message)
            out.writerow(row)

    if isinstance(outfile, str):
        outf.close()


if __name__ == '__main__':
    main()
