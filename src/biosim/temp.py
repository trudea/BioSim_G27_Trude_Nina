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
herman.weight = 2
print(herman.phi)
herman.weight = 50
herman.evaluate_fitness()
print(herman.phi)

