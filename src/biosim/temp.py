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

for i in range(50):
    island.all_cells('replenish')
    island.all_cells('feeding')
    island.all_cells('procreation')
    island.migration()
    island.all_cells('dying')
    island.update_num_animals()
    print(island.num_animals_per_species)

    #island.update_num_animals()





