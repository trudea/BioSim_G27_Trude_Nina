from math import exp
import random
import numpy as np

from src.biosim.landscapes import Savannah, Jungle, Desert, Mountain, Ocean
from src.biosim.animals import Herbivore, Carnivore
from src.biosim.island import Island

a = 'b = 1 + 2'
exec(a)
print(b)
island = Island()
print(island.map_dict[(1,1)])
