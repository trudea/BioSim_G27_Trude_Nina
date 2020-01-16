from math import exp
import random
import numpy as np

from src.biosim.landscapes import Savannah, Jungle, Desert, Mountain, Ocean
from src.biosim.animals import Herbivore, Carnivore
from src.biosim.island import Island

#from src.biosim.landscapes import *
import src.biosim.animals as animals

carl = Carnivore()
herman = Herbivore()
map = 'OOOOOOO\nOSSSSSO\nOSSSSSO\nOSSSSSO\nOSSSSSO\nOSSSSSO\nOOOOOOO'
simple_island = Island(map)
for cell in simple_island.map.values():
    for species in cell.pop:
        cell.pop[species].append(eval(species)())
        cell.pop[species].append(eval(species)())
        cell.pop[species].append(eval(species)())
        cell.pop[species].append(eval(species)())
        cell.pop[species].append(eval(species)())
print()



