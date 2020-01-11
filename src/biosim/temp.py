from math import exp
import random
import numpy as np
from animals import Herbivore, Carnivore
from landscapes import Savannah, Jungle, Mountain, Desert, Ocean
from island import Island, Cell, AdjacentCell

exis = 'OOOOSOOOO'

c = Cell(1,1)
print(c)

ex = [{'loc':(1,1), 'pop': {'species': Herbivore, 'age': 10, 'weight': 12.5}}]

def place_animals(self, input_list):
    ani_dict = {'Herbivore': Herbivore, 'Carnivore': Carnivore}
    for placement_dict in input_list:
        y, x = placement_dict['loc']
        for individual in placement_dict['pop']:
            self.map[y][x].pop.append(
                ani_dict[individual['species']](individual))