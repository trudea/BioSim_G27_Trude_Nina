from math import exp
import random
import numpy as np

from src.biosim.landscapes import Savannah, Jungle, Desert, Mountain, Ocean
from src.biosim.animals import Herbivore, Carnivore
from src.biosim.island import Island, Cell

"""
from BioSim_G27_Trude_Nina.biosim.animals import Herbivore, Carnivore
from .landscapes import Savannah, Jungle, Mountain, Desert, Ocean
from .island import Island, Cell
"""
temp = {'banan': 1, 'eple': 2}




i = Island()
c = Cell(1,1, 'S')
herman = Herbivore()
c.pop.append(herman)
i.choose_new_cell(c, herman)
carl = Carnivore()


input = [{'loc': (3, 4), 'pop': [
            {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
            {'species': 'Herbivore', 'age': 9, 'weight': 10.3}]}]
i.place_animals(input)
c = i.map[3][4]


herman = Herbivore({'age' : 9})
hermine = Herbivore({'age': 7})
herbert = Herbivore({'age' : 1})
pop = [herman, hermine, herbert]
for i in pop:
    print(i.age)
pop = sorted(pop, key=lambda x: getattr(x, 'age'))
for i in pop:
    print(i.age)