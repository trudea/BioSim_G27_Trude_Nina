# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

import numpy as np
from math import exp
import random
from .landscapes import Savannah, Jungle, Ocean, Mountain, Desert
from .animals import Herbivore, Carnivore


class Island:
    land_dict = {'S': Savannah, 'J': Jungle,
                 'O': Ocean, 'M': Mountain, 'D': Desert}

    def string_to_array(self, txt):
        # bør kanskje importeres
        if txt[-1] is not "\n":
            txt += "\n"
        line, lines = [], []
        y, x = 0, 0
        for letter in txt:
            if letter in self.land_dict:
                line.append(letter)
                x += 1
            if letter == "\n":
                lines.append(line)
                line = []
                y += 1
                x = 0
        return np.asarray(lines)

    def str_to_dict(self, txt):
        txt = txt.split('\n')
        if txt[-1] == '\n':
            txt = txt.pop()
        y = 0
        x = 0
        dict = {}
        for row in txt:
            x=0
            for letter in row:
                dict[(y, x)] = self.land_dict[letter]()
                print(y, ' ', x)
                x += 1
            y += 1
        return dict



    def check_edges(self):
        left_column = [line[0] for line in self.map]
        right_column = [line[-1] for line in self.map]
        to_check = [self.map[0], self.map[-1], left_column, right_column]
        for list in to_check:
            for element in list:
                if element != 'O':
                    raise ValueError

    def __init__(self, txt=None):
        self.num_animals = 0
        self.num_animals_per_species = {'Herbivore' : 0, 'Carnivore': 0}
        if txt is None:
            txt = open('rossum.txt').read() # med \n som siste argument
        self.map = self.string_to_array(txt)  # array of one-letter-strings
        self.map_dict = self.str_to_dict(txt)



        self.check_edges()
        island_line = []
        island_lines = []
        """
        for y, line in enumerate(self.map):
            for x, letter in enumerate(line):

                island_line.append(self.land_dict[letter]())
            island_lines.append(island_line)
            island_line = []
            """
        self.map = np.array(island_lines)


    def all_cells(self, myfunc):
        for row in self.map:
            for cell in row:
                cell.myfunc()

    def replenish_all(self):
        for row in self.map:
            for cell in row:
                cell.replenish

    def all_animals(self, myfunc):
        for row in self.island.map:
            for cell in row:
                for animal in cell.pop:
                    myfunc(animal)



    def place_animals(self, input_list):
        ani_dict = {'Herbivore': Herbivore, 'Carnivore': Carnivore}

        for placement_dict in input_list:
            pos = placement_dict['loc']
            for individual in placement_dict['pop']:
                new_animal = ani_dict[individual['species']](individual) # bruke exec?
                self.map_dict[pos].pop.append(new_animal)
                self.map_dict[(pos)].tot_w_herbivores += new_animal.weight


    def remove_animal(self, cell, animal):
        cell.pop.remove(animal)

    def move_animal(self, old_cell, new_cell, animal):
        new_cell.pop.append(animal)
        old_cell.pop.remove(animal) # use filtering?

    def migration(self):
        moving_animals = [] # evt dictionary
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                for animal in cell.pop:
                    if animal.check_if_moves: # endre navn slik at animal.moves?
                        new_cell = self.choose_new_cell(y, x, type(animal))


                        moving_animals.append(animal, new_cell)
                moving_animals.append(cell.migration()) # returnerer liste av dictionaries av dyr som vil ut av cellen, med nye posisjoner
        place_animals(moving_animals)

    def choose_new_position(self, y, x, animaltype):
        positions = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
        #possible_cells = [self.map[y-1][x], self.map[y+1][x], self.map[y][x-1], self.map[y][x+1]]
        pos_dict = {}
        for position in positions:
            self.map_dict[position].get_rel_abundance(animaltype)
            self.map_dict[position].get_propensity()
        total_propensity = sum([self.map_dict[position].propensity for position in positions])
        for position in positions:
            self.map_dict[position].likelihood = self.map_dict[position].propensity / total_propensity

        chosen_cell = np.random.choice(positions, 1000, p=[positions.probability for position in positions])
        for candidate in positions:
            candidate.rel_abundance = None
            candidate.propensity = None
        return chosen_cell












        """
        keys = temp_dict.keys()
        for key in keys:
            temp_dict[key]['probability'] = \
                temp_dict[key]['propensity'] / total_propensity
        remembered_limit = 0

        for key in keys:
            temp_dict[key]['lower_limit'] = remembered_limit
            temp_dict[key]['upper_limit'] =\
                remembered_limit + temp_dict[key]['probability']
            remembered_limit = temp_dict[key]['upper_limit']
        number = round(random.random(), 7)
        for key in keys:
            if temp_dict[key]['lower_limit'] < \
                    number < temp_dict[key]['upper_limit']:
                return key
        """
