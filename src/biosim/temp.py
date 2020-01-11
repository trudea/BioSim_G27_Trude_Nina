from math import exp
import random
import numpy as np
from animals import Herbivore, Carnivore
from landscapes import Savannah, Jungle, Mountain, Desert, Ocean

def death(param_dict, phi):
    probability = round(param_dict['omega'] * (1 - phi), 3)
    if phi == 0 or round(random.random(), 3) >= probability:
        return True
    else:
        return False


herman = Herbivore()
scar = Carnivore()
herman.phi = 0.1
scar.phi = 1
a = scar.check_if_kills(herman)
print(a)

