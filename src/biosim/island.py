# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

import numpy as np
from math import exp
import random
from .landscapes import Savannah, Jungle, Ocean, Mountain, Desert
from .animals import Herbivore, Carnivore, bubble_sort_animals


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
            txt = open('rossum.txt').read()
            if txt[-1] == "\n":
                # legg inn noe som fjerner siste element hvis det er formen
                # vi vil ha det på senere
                pass
        self.map = self.string_to_array(txt)  # array of one-letter-strings
        self.check_edges()
        island_line = []
        island_lines = []
        for y, line in enumerate(self.map):
            for x, letter in enumerate(line):

                island_line.append(self.land_dict[letter]())
            island_lines.append(island_line)
            island_line = []
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
            y, x = placement_dict['loc']
            for individual in placement_dict['pop']:
                new_animal = ani_dict[individual['species']](individual)
                self.map[y][x].pop.append(new_animal)
                self.map[y][x].tot_w_herbivores += new_animal.weight


    def remove_animal(self, cell, animal):
        cell.pop.remove(animal)

    def move_animal(self, old_cell, new_cell, animal):
        new_cell.pop.append(animal)
        old_cell.pop.remove(animal) # use filtering?

    def migration(sef):
        moving_animals = [] # evt dictionary
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                for animal in cell.pop:
                    if animal.check_if_moves: # endre navn slik at animal.moves?
                        new_cell = choose_new_cell(y, x)
                        moving_animals.append(animal, )
                moving_animals.append(cell.migration()) # returnerer liste av dictionaries av dyr som vil ut av cellen, med nye posisjoner
        place_animals(moving_animals)


     def choose_new_cell(y, x, animal):
            #y, x = cell.get_position() # beste
            y, x = self.get_position()
            possible_cells = [self.map[y-1][x], self.map[y+1][x], self.map[y][x-1],
                              self.map[y][x+1]]
            for element in possible_cells:
                if type(element.landscape) == Ocean: # use filtering
                    possible_cells.remove(element)
                elif type(element.landscape) == Mountain:
                    possible_cells.remove(element)
            if len(possible_cells) == 0:
                return False
            elif len(possible_cells) == 1:
                return possible_cells[0]
            temp_dict = {}
            for element in possible_cells:
                rel_abund = element.get_rel_abundance(animal)
                temp_dict[element] = \
                    {'propensity': exp(animal.lambdah * rel_abund)}
            total_propensity = \
                sum([temp_dict[element]['propensity'] for element in temp_dict])
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

