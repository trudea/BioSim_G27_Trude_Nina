# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

import inspect
import numpy as np
from biosim.landscapes import Savannah, Jungle, Ocean, Mountain, Desert
from biosim.animals import Herbivore, Carnivore
import biosim.animals as animals


class Island:
    # ta høyde for store og små bokstaver
    land_dict = {'S': Savannah, 'J': Jungle,
                 'O': Ocean, 'M': Mountain, 'D': Desert}

    def __init__(self, txt=None):
        self.num_animals = 0
        self.num_animals_per_species = {'Herbivore': 0, 'Carnivore': 0}
        if txt is None:
            txt = open('rossum.txt').read()  # med \n som siste argument
        self.map = self.str_to_dict(txt)

    def str_to_dict(self, txt):
        txt = txt.splitlines()
        if txt[-1] == '\n':
            txt = txt.pop()
        self.check_all(txt)

        y = 0
        dict = {}
        for row in txt:
            x = 0
            for letter in row:
                dict[(y, x)] = self.land_dict[letter]()
                x += 1
            y += 1
        return dict

    @staticmethod
    def check_all(txt):
        valid = ['O', 'S', 'J', 'D', 'M']
        right_edge = [line[-1] for line in txt]
        left_edge = [line[0] for line in txt]
        edges = [txt[0][:], txt[-1][:], right_edge, left_edge]
        edges_list = [letter for edge in edges for letter in edge]

        for i in txt:
            if len(i) != len(txt[0]):
                raise ValueError('Map lines not same length')

        for letter in edges_list:
            if letter != 'O':
                raise ValueError('Map has to be surrounded by ocean')

        for line in txt:
            for letter in line:
                if letter not in valid:
                    raise ValueError('Invalid landscape type')

    def all_cells(self, myfunc):
        for cell in self.map.values():
            getattr(cell, myfunc)()

    def all_animals(self, myfunc):
        for cell in self.map.values():
            for species in cell.pop:
                for animal in cell.pop[species]:
                    getattr(animal, myfunc)()

    def place_animals(self, input_list):
        for placement_dict in input_list:
            pos = placement_dict['loc'] # bør flytte resten til celle?
            self.map[pos].place_animals(placement_dict['pop'])

    def migration(self): # husk filtering
        for pos, cell in self.map.items():
            if type(cell) == Ocean or type(cell) == Mountain:
                pass
            else:
                y, x = pos
                adjecent_pos = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)] # må ta høyde for edges
                map_list = [self.map[element] for element in adjecent_pos]
                for element in map_list:
                    if type(element) == Ocean or type(element) == Mountain:
                        map_list.remove(element)
                cell.migration(map_list)

    def update_num_animals(self):
        self.num_animals = 0
        self.num_animals_per_species = {'Herbivore': 0, 'Carnivore': 0}
        for cell in self.map.values(): # bør kunne flyttes inn
            self.num_animals += cell.num_animals()
            for species in self.num_animals_per_species:
                self.num_animals_per_species[species] +=\
                    cell.num_animals_per_species()[species]


if __name__ == '__main__':
    map = 'OOOO\nOJJO\nOOOO'
    Island(map)