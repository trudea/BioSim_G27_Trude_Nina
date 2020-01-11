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
        self.y = y
        self.x = x
        self.herb_pop = [] # instances av Herbivore i celle
        self.carn_pop = [] # instances av Carnivore i celle
        self.pop = []

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

    def num_specimen_in_cell(cell, species): # privat? burde være i island
        n = 0
        for animal in cell.pop:
            if type(animal)==species:
                n+=1
        return n


    def procreation(self):
        pass

    def migration(self):
        pass

