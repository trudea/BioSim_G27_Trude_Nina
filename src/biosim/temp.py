from math import exp
import random
import numpy as np

from src.biosim.landscapes import Savannah, Jungle, Desert, Mountain, Ocean
from src.biosim.animals import Herbivore, Carnivore
from src.biosim.island import Island

#from src.biosim.landscapes import *
import src.biosim.animals as animals

s = Savannah()
s.f = 0.3
getattr(s, 'replenish')()
print(s.f)