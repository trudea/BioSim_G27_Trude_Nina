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
print(carl.phi, ' ', herman.phi)
print(carl.check_if_kills(herman))