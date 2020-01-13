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
        #self.map = self.string_to_array(txt)  # array of one-letter-strings
        self.map = self.str_to_dict(txt) # DICTIONARY



        # self.check_edges()
        # island_line = []
        # island_lines = []
        """
        for y, line in enumerate(self.map):
            for x, letter in enumerate(line):

                island_line.append(self.land_dict[letter]())
            island_lines.append(island_line)
            island_line = []
            """
        #self.map = np.array(island_lines)


    def all_cells(self, myfunc):
        for row in self.map:
            for cell in row:
                cell.myfunc()

    def replenish_all(self):
        for cell in self.map:
            self.map[cell].replenish()

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
                self.map[pos].pop.append(new_animal)
                self.map[(pos)].tot_w_herbivores += new_animal.weight


    def remove_animal(self, cell, animal):
        cell.pop.remove(animal)

    def move_animal(self, old_cell, new_cell, animal):
        new_cell.pop.append(animal)
        old_cell.pop.remove(animal) # use filtering?

    def migration(self):
        copy = self.map
        for pos in self.map:
            for animal in self.map[pos].pop:
                if animal.check_if_moves: # endre navn slik at animal.moves?
                    new_cell = self.choose_new_pos(pos, animal)
                    new_cell.pop.append(animal)
                    self.map[pos].pop.remove(animal)

    def choose_new_pos(self, position, animal):
        y, x = position
        list = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
        map_list = [self.map[element] for element in list]
        for pos in map_list:
            pos.get_rel_abundance(animal)
            pos.get_propensity(animal)
        total_propensity = sum([pos.propensity for pos in map_list])
        for pos in map_list:
            pos.likelihood = pos.propensity / total_propensity
        choices = np.random.choice(map_list, 1000, p=[pos.likelihood for pos in map_list])
        chosen_cell = np.random.choice(choices)
        for candidate in map_list:
            candidate.rel_abundance = None
            candidate.propensity = None
        return chosen_cell

    def update_num_animals(self):
        self.num_animals = 0
        self.num_animals_per_species = {'Herbivore' : 0, 'Carnivore' : 0}

        for cell in self.map.values():
            cell.update_num_animals()
            self.num_animals += cell.num_animals
            for species in self.num_animals_per_species:
                self.num_animals_per_species[species] += cell.num_animals_per_species[species]