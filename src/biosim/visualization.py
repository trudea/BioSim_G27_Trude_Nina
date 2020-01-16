# -*- coding: utf-8 -*-

"""
Features:
biomass, gjennomsnittsalder for hver art, gjennomsnittlig dødsalder,
vekstrate per år (antall døde - antall fødte)
antall døde per år
antall fødte hvert år

"""
from biosim.animals import Carnivore, Herbivore

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"


from biosim.island import Island
import biosim.run as r
import matplotlib.pyplot as plt
import numpy as np
import random

carnivore_list = [{'loc': (1, 1), 'pop': [
        {'species': 'Carnivore', 'age': 10, 'weight': 40.5},
        {'species': 'Carnivore', 'age': 9, 'weight': 38.3},
        {'species': 'Carnivore', 'age': 14, 'weight': 50.3},
        {'species': 'Carnivore', 'age': 5, 'weight': 36.1}]},
               {'loc': (2, 2), 'pop': [
                   {'species': 'Herbivore', 'age': 10, 'weight': 40.5},
                   {'species': 'Herbivore', 'age': 9, 'weight': 38.3},
                   {'species': 'Herbivore', 'age': 14, 'weight': 50.3},
                   {'species': 'Herbivore', 'age': 5, 'weight': 36.1}]}

               ]

counter = 0
"""
while counter > 0:
    simulation.one_cycle()
    species = simulation.per_species_results
    herbivores = []
    carnivores = []

    for i in species:
        herbivores.append(i["Herbivore"])

    for s in species:
        carnivores.append(s["Carnivore"])
    if counter == 100:
        simulation.island.place_animals(carnivore_list)

    plt.plot([x for x in range(len(simulation.per_species_results))],
             [carnivores[i] for i in
              range(len(simulation.num_animals_results))],
             'r-', label="Carnivores")

    plt.plot([x for x in range(len(simulation.per_species_results))],
             [herbivores[i] for i in range(len(
                 herbivores))], 'g-', label="Herbivores")
    plt.xlabel("Years")
    plt.ylabel("Population")
    plt.title("Biosimulator")
    plt.legend()
    plt.pause(0.1)
    plt.show()
    counter -= 1
"""
herbivores = []
carnivores = []
simulation = r.Run()
while counter < 500:
    simulation.one_cycle()
    if counter == 50:
        simulation.island.place_animals(carnivore_list)
    counter += 1

    species = simulation.per_species_results
for i in species:
    herbivores.append(i["Herbivore"])

for s in species:
    carnivores.append(s["Carnivore"])

plt.plot([x for x in range(len(simulation.per_species_results))],
        [carnivores[i] for i in
        range(len(simulation.num_animals_results))],
         'r-', label="Carnivores")

plt.plot([x for x in range(len(simulation.per_species_results))],
        [herbivores[i] for i in range(len(
        herbivores))], 'g-', label="Herbivores")
plt.xlabel("Years")
plt.ylabel("Population")
plt.title("Biosimulator")
plt.legend()
plt.pause(0.1)
plt.show()


"""
kart = """

"""
#                   R    G    B
rgb_value = {'O': (0.0, 0.0, 1.0),  # blue
             'M': (0.5, 0.5, 0.5),  # grey
             'J': (0.0, 0.6, 0.0),  # dark green
             'S': (0.5, 1.0, 0.5),  # light green
             'D': (1.0, 1.0, 0.5)}  # light yellow

kart_rgb = [[rgb_value[column] for column in row]
            for row in kart.splitlines()]

fig = plt.figure()

axim = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h
axim.imshow(kart_rgb)
axim.set_xticks(range(len(kart_rgb[0])))
axim.set_xticklabels(range(1, 1 + len(kart_rgb[0])))
axim.set_yticks(range(len(kart_rgb)))
axim.set_yticklabels(range(1, 1 + len(kart_rgb)))

axlg = fig.add_axes([0.85, 0.1, 0.1, 0.8])  # llx, lly, w, h
axlg.axis('off')
for ix, name in enumerate(('Ocean', 'Mountain', 'Jungle',
                           'Savannah', 'Desert')):
    axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                 edgecolor='none',
                                 facecolor=rgb_value[name[0]]))
    axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

plt.show()
"""