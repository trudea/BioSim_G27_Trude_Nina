from math import exp
import random
import numpy as np

from src.biosim.landscapes import Savannah, Jungle, Desert, Mountain, Ocean
from src.biosim.animals import Herbivore, Carnivore
from src.biosim.island import Island

#from src.biosim.landscapes import *
import src.biosim.animals as animals

import random

map = 'OOOOOOO\nOJJJJJO\nOJJJJJO\nOJJJJJO\nOJJJJJO\nOJJJJJO\nOJJJJJO\nOOOOOOO'
random.seed(33)
island = Island(map)
cell = island.map[(1,1)]
for i in range(5):
    cell.pop['Herbivore'].append(Herbivore())
    cell.pop['Herbivore'].append(Herbivore())
    cell.pop['Herbivore'].append(Herbivore())
cell = island.map[(2,2)]
for i in range(5):
    cell.pop['Herbivore'].append(Herbivore())
    cell.pop['Herbivore'].append(Herbivore())
    cell.pop['Herbivore'].append(Herbivore())
cell = island.map[(1,2)]
for i in range(5):
    cell.pop['Herbivore'].append(Herbivore())
    cell.pop['Herbivore'].append(Herbivore())
    cell.pop['Herbivore'].append(Herbivore())
cell = island.map[(2,1)]
for i in range(5):
    cell.pop['Herbivore'].append(Herbivore())
    cell.pop['Herbivore'].append(Herbivore())
    cell.pop['Herbivore'].append(Herbivore())

def list_herbivores():
    all_herbivores = []
    for cell in island.map.values():
        if len(cell.pop['Herbivore']) > 0:
            for element in cell.pop['Herbivore']:
                all_herbivores.append(element)
    return all_herbivores

island.update_num_animals()
#print(island.num_animals_per_species)
for i in range(2):
    island.all_cells('replenish')
    for i in [type(cell) == Jungle for cell in island.map.values()]:
        if cell.f != 800.0:
            print('Not replenished')
    copy = list_herbivores()
    island.all_cells('feeding')
    for cell in [cell for cell in island.map.values() if type(cell) == Jungle]:
        # print(cell.f)
        if cell.f == 800.0 and len(cell.pop['Herbivore']) > 0:
            print('Not consumed')
    all_herbivores = list_herbivores()
    weights = [herbivore.weight for herbivore in all_herbivores]
    for i in range(len(copy)):
        # print(weights[i] - copy[i].weight)
        pass
    all_herbivores = list_herbivores()
    print(len(all_herbivores))
    island.all_cells('procreation')
    all_herbivores = list_herbivores()
    print(len(all_herbivores))
    # island.migration()
    # island.all_cells('dying')
    island.update_num_animals()
    # print(island.num_animals_per_species)

    #island.update_num_animals()
    pass





