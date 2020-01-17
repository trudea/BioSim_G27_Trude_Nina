from math import exp
import random
import numpy as np

from src.biosim.landscapes import Savannah, Jungle, Desert, Mountain, Ocean
from src.biosim.animals import Herbivore, Carnivore
from src.biosim.island import Island

#from src.biosim.landscapes import *
import src.biosim.animals as animals
import src.biosim.island as island
from src.biosim.run import Run

simple_map = 'OOOO\nOJJO\nOOOO'
simple_herbs = []
simple_herb_list = [Herbivore() for i in range(50)]
for h in simple_herb_list:
    simple_herb = {}
    simple_herb['species'] = 'Herbivore'
    simple_herb['age'] = h.age
    simple_herb['weight'] = h.weight
    simple_herbs.append(h)
simple_herb_pop = [{'loc': (1,1), 'pop' : simple_herbs}]

mocker.patch('random.random', return_value=0.001)
herbivores = [ani.Herbivore({'phi': 0.1}), ani.Herbivore({'phi': 0.5}),
              ani.Herbivore({'phi': 0.9})]
c = Carnivore({'phi': 0.5})
c.feeding()
