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
carl = Carnivore()
carl.weight = 2
carla = Carnivore()
carla.weight = 2
camille = Carnivore()
camille.weight = 2
herbert = Herbivore()
herbert.weight = 1
hermine = Herbivore()
hermine.weight = 1
herman = Herbivore()
herman.weight = 1

liste = [carl, carla, camille, herbert, hermine, herman]
weights = sum([animal.weight for animal in liste if type(animal)==Carnivore])

a = 1
b = 3
c = 2

if c == a or b:
    print(True)