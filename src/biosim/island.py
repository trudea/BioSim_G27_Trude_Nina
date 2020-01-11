# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"


# import animal.py
import numpy as np
from math import exp
import random
from landscapes import Savannah, Jungle, Ocean, Mountain, Desert
from animals import Herbivore, Carnivore, bubble_sort_animals


class Cell:
    land_dict = {'S': Savannah, 'J': Jungle, 'O': Ocean, 'M': Mountain,
                     'D': Desert}
    def __init__(self, y, x, letter):
        self.landscape = self.land_dict[letter]()
        # self.y = y
        # self.x = x
        self.pos = (y, x) # using this
        self.pop = []
        self.tot_w_herbivores = sum([animal.weight for animal in self.pop if type(animal)==Herbivore])

    def num_specimen_in_cell(self, species):  # privat? burde kanskje være utenfor?
        n = 0
        for animal in self.pop:
            if type(animal) == species:
                n += 1
        return n


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



    def rel_abundance(self, cell, animal, N): # er noe kluss med at fodder avhenger av art
        if type(animal) == Herbivore:
            fodder = cell.f
        if type(animal) == Carnivore:
            fodder = cell.tot_w_herbivores
        return fodder / ((N + 1) * animal.F)

    def propensity(self, cell, animal, rel_abund):
        if type(cell) == Mountain or type(cell) == Ocean: # unødvendig fordi de ikke ble lagt til i adj-lista?
            return 0
        else:
            return exp(animal.lambdah * rel_abund)

    def __init__(self, txt=None):
        if txt is None:
            txt = open('rossum.txt').read()
            if txt[-1] == "\n":
                #legg inn noe som fjerner siste element hvis det er formen vi vil ha det på senere
                pass
        self.map = self.string_to_array(txt) # array of one-letter-strings
        self.check_edges()
        # creating array of cells
        island_line = []
        island_lines = []
        for y, line in enumerate(self.map):
            for x, letter in enumerate(line):
                island_line.append(Cell(y, x, letter))
            island_lines.append(island_line)
            island_line = []
        self.map = np.array(island_lines)

    def place_animals(self, input_list):
        ani_dict = {'Herbivore': Herbivore, 'Carnivore': Carnivore}
        for placement_dict in input_list:
                y, x = placement_dict['loc']
                for individual in placement_dict['pop']:
                    self.map[y][x].pop.append(ani_dict[individual['species']](individual))

    def remove_animal(self, cell, animal):
        cell.pop.remove(animal)

    def choose_new_cell(self, cell, animal):
        N = self.num_specimen_in_cell(cell, type(animal))
        adj_cells ={}
        y, x = cell.pos
        for row in self.map:
            for other_cell in row:
                if type(other_cell) == Savannah or type(other_cell) == Jungle or type(other_cell) == Desert:
                    if (other_cell.pos[0] == y-1 or other_cell.pos[0] == y+1 and
                            other_cell.pos[1] == x-1 or other_cell.pos[1] == x+1):
                        adj_cells[other_cell] = {}
        if len(adj_cells) > 0:
            for adj_cell in adj_cells:
                rel_abund = rel_abund(adj_cell, animal, N)
                propensity = propensity(adj_cell, animal, rel_abund)
                adj_cells[adj_cell]['propensity'] = propensity
            for adj_cell in adj_cells:
                adj_cell['probability'] = adj_cell['propensity'] / sum([element[propensity] for element in adj_cells ])

    def move_animal(self, old_cell, new_cell, animal):
        new_cell.pop.append(animal)
        old_cell.pop.remove(animal)