from math import exp
import random
import numpy as np
from animals import Herbivore, Carnivore
from landscapes import Savannah, Jungle, Mountain, Desert, Ocean
from island import Island, Cell, AdjacentCell

exis = 'OOOOSOOOO'



i = Island()
c = Cell(1,1, 'S')
herman = Herbivore()
c.pop.append(herman)
i.choose_new_cell(c, herman)
