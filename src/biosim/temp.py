from math import exp
import random
import numpy as np
from animals import Herbivore, Carnivore
from landscapes import Savannah, Jungle, Mountain, Desert, Ocean
from island import Island, Cell, AdjacentCell

temp = {'banan': 1, 'eple': 2}
for element in temp:
    print(element)



i = Island()
c = Cell(1,1, 'S')
herman = Herbivore()
c.pop.append(herman)
i.choose_new_cell(c, herman)
