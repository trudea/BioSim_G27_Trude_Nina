from math import exp
import random
import numpy as np
from animals import Herbivore, Carnivore
from landscapes import Savannah, Jungle, Mountain, Desert, Ocean
from island import Island, Cell

def death(param_dict, phi):
    probability = round(param_dict['omega'] * (1 - phi), 3)
    if phi == 0 or round(random.random(), 3) >= probability:
        return True
    else:
        return False


island = Island()
c = Cell(0,0,'S')
c.pop.append(Herbivore())
x = Island.num_specimen_in_cell(c, Herbivore)
print(x)