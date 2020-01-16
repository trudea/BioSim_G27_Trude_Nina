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
map = "OOO\nORO\nOOO"
# map = 'OOOOOOO\nOJJJJJO\nOJJJJJO\nOJJJJJO\nOJJJJJO\nOJJJJJO\nOOOOOOO'
simple_island = Island(map)
herman = Herbivore()
cell = simple_island.map[3,3]
for i in range(20):
    cell.pop['Herbivore'].append(Herbivore)
cell.procreation()


