# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"


import random
from src.biosim.animals import Carnivore, Herbivore
import matplotlib.pyplot as plt
import inspect
import numpy as np
from .landscapes import Savannah, Jungle, Ocean, Mountain, Desert
from .animals import Herbivore, Carnivore
import src.biosim.animals as animals


class Island:
    # ta høyde for store og små bokstaver
    land_dict = {'S': Savannah, 'J': Jungle,
                 'O': Ocean, 'M': Mountain, 'D': Desert}

    def str_to_dict(self, txt):
        txt = txt.split('\n')
        print(txt[-1])
        if txt[-1] == '\n':
            txt = txt.pop()
        txt.pop()
        print(txt[-1]) # midlertidig
        for line in txt:
            if len(line) != len(txt[0]):
                raise ValueError
        #self.check_letters(txt)
        self.check_edges(txt)
        #self.check_letters(txt)
        valid = ['O', 'S', 'J', 'D', 'M']
        for row in txt:
            for letter in row:
                if letter not in valid:
                    raise ValueError

        y = 0
        dict = {}
        for row in txt:
            x = 0
            for letter in row:
                dict[(y, x)] = self.land_dict[letter]()
                x += 1
            y += 1
        return dict

    def check_letters(self, txt):
        valid = ['O', 'S', 'J', 'D', 'M']
        length_line = []
        for line in txt:
            length_line.append(len(line))
            for letter in txt:
                if letter not in valid:
                    raise ValueError
                if [length for length in length_line] != len(line):
                    raise ValueError

    def check_edges(self, txt):
        left_column = [line[0] for line in txt]
        right_column = [line[-1] for line in txt]
        to_check = [txt[0], txt[-1], left_column, right_column]
        for list in to_check:
            for element in list:
                if element != 'O':
                    raise ValueError

    def __init__(self, txt=None):
        self.num_animals = 0
        self.num_animals_per_species = {'Herbivore': 0, 'Carnivore': 0}
        if txt is None:
            txt = open('rossum.txt').read()  # med \n som siste argument
        self.map = self.str_to_dict(txt)

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

class Run:
    default_input = [{'loc': (3, 4), 'pop': [
        {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
        {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
        {'species': 'Carnivore', 'age': 14, 'weight': 10.3},
        {'species': 'Carnivore', 'age': 5, 'weight': 10.1}]},
                     {'loc': (4, 4),
                      'pop': [
                          {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
                          {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
                          {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]}]
    herbivore_input = [{'loc': (3, 4), 'pop': [
        {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
        {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
        {'species': 'Herbivore', 'age': 14, 'weight': 10.3},
        {'species': 'Herbivore', 'age': 5, 'weight': 10.1}]},
                     {'loc': (4, 4),
                      'pop': [
                          {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
                          {'species': 'Herbivore', 'age': 3, 'weight': 7.3},
                          {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]}]

    def __init__(self, ini_pop=None, island_map=None, seed=None):

        self.desired_years = 10
        self.num_animals_results = []
        self.per_species_results = []
        if ini_pop is None:
            ini_pop = self.herbivore_input
        self.island = Island(island_map)
        self.island.place_animals(ini_pop)
        self.years = 0

    def one_cycle(self):
        self.island.all_cells('replenish')
        self.island.all_cells('feeding')
        self.island.all_cells('procreation')
        self.island.migration()
        self.island.all_animals('aging')
        self.island.all_animals('weightloss')
        self.island.all_cells('dying')
        self.island.update_num_animals()
        self.num_animals_results.append(self.island.num_animals)
        self.per_species_results.append(self.island.num_animals_per_species)
        self.years += 1

    def run(self):
        self.years = 0
        self.desired_years = 50
        while(self.years < self.desired_years):
            print(run.island.num_animals_per_species)
            self.one_cycle()
            self.years += 1



if __name__ == "__main__":
    # map = 'OOOOO\nOJJJO\nOJJJO\nOJJJO\nOJJJO\nOOOO'
    animals = [{'loc': (1, 1), 'pop': [
        {'species': 'Herbivore', 'age': 10, 'weight': 40.5},
        {'species': 'Herbivore', 'age': 9, 'weight': 38.3},
        {'species': 'Herbivore', 'age': 14, 'weight': 50.3},
        {'species': 'Herbivore', 'age': 5, 'weight': 36.1}]},
               {'loc': (2, 2), 'pop': [
                   {'species': 'Herbivore', 'age': 10, 'weight': 40.5},
                   {'species': 'Herbivore', 'age': 9, 'weight': 38.3},
                   {'species': 'Herbivore', 'age': 14, 'weight': 50.3},
                   {'species': 'Herbivore', 'age': 5, 'weight': 36.1}]}

               ]

    # map = 'OOOOOOO\nOJJJJJO\nOJJJJJO\nOJJJJJO\nOJJJJJO\nOJJJJJO\nOJJJJJO\nOOOOOOO'

    # island = Island()
    run = Run()
    """
    cell = run.island.map[(1, 1)]
    for i in range(5):
        cell.pop['Herbivore'].append(Herbivore())
        cell.pop['Herbivore'].append(Herbivore())
        cell.pop['Herbivore'].append(Herbivore())
    cell = run.island.map[(2, 2)]
    for i in range(5):
        cell.pop['Herbivore'].append(Herbivore())
        cell.pop['Herbivore'].append(Herbivore())
        cell.pop['Herbivore'].append(Herbivore())
    cell = run.island.map[(1, 2)]
    for i in range(5):
        cell.pop['Herbivore'].append(Herbivore())
        cell.pop['Herbivore'].append(Herbivore())
        cell.pop['Herbivore'].append(Herbivore())
    cell = run.island.map[(2, 1)]
    for i in range(5):
        cell.pop['Herbivore'].append(Herbivore())
        cell.pop['Herbivore'].append(Herbivore())
        cell.pop['Herbivore'].append(Herbivore())


    def list_herbivores():
        all_herbivores = []
        for cell in run.island.map.values():
            if len(cell.pop['Herbivore']) > 0:
                for element in cell.pop['Herbivore']:
                    all_herbivores.append(element)
        return all_herbivores


    def list_carnivores():
        all_carnivores = []
        for cell in run.island.map.values():
            if len(cell.pop['Carnivore']) > 0:
                for element in cell.pop['Carnivore']:
                    all_carnivores.append(element)
        return all_carnivores

    run.run()

    for i in range(100):
        run.island.map[(1, 1)].pop['Carnivore'].append(Carnivore())
        run.island.map[(2, 2)].pop['Carnivore'].append(Carnivore())
        run.island.map[(3, 3)].pop['Carnivore'].append(Carnivore())
        run.island.map[(1, 1)].pop['Carnivore'].append(Carnivore())
        run.island.map[(2, 2)].pop['Carnivore'].append(Carnivore())
        run.island.map[(3, 3)].pop['Carnivore'].append(Carnivore())
        run.island.map[(1, 1)].pop['Carnivore'].append(Carnivore())
        run.island.map[(2, 2)].pop['Carnivore'].append(Carnivore())
        run.island.map[(3, 3)].pop['Carnivore'].append(Carnivore())
        run.island.map[(1, 1)].pop['Carnivore'].append(Carnivore())
        run.island.map[(2, 2)].pop['Carnivore'].append(Carnivore())
        run.island.map[(3, 3)].pop['Carnivore'].append(Carnivore())
    run.island.update_num_animals()
    # print(run.island.num_animals_per_species)
    """
    run.run()
