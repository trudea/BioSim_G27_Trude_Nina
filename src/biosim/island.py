# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

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
        # burde ha check_edges som en egen funksjon?
        txt = txt.split('\n')
        if txt[-1] == '\n':
            txt = txt.pop()
        edges = txt[0] + txt[-1]
        for letter in txt[0]:
            if letter != 'O':
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
        self.num_animals_per_species = {'Herbivore': 0, 'Carnivore': 0}
        if txt is None:
            txt = open('rossum.txt').read()  # med \n som siste argument
        self.map = self.str_to_dict(txt)
        #self.species_to_class = dict(inspect.getmembers(animals, inspect.isclass))
        # del self.species_to_class['Animal']

    def all_cells(self, myfunc):
        for cell in self.map.values():
            getattr(cell, myfunc)()
        self.update_num_animals()

    def all_animals(self, myfunc):
        for cell in self.map.values():
            for species in cell.pop:
                for animal in cell.pop[species]:
                    getattr(animal, myfunc)()
        self.update_num_animals()



    def place_animals(self, input_list):
        for placement_dict in input_list:
            pos = placement_dict['loc'] # bør flytte resten til celle?
            self.map[pos].place_animals(placement_dict['pop'])
        self.update_num_animals()


# ENDRINGER


    def migration(self): # husk filtering
        for cell in self.map:
            print(self.map((0,0)))
            print(self.map(cell))
            if type(self.map(cell)) != Ocean and type(self.map(cell)) != Mountain:
                y, x = cell
                print((y, x))
                print('hi')
                adjecent_pos = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)] # må ta høyde for edges
                map_list = [self.map[element] for element in adjecent_pos]
                for element in map_list:
                    if type(element) == Ocean or type(element) == Mountain:
                        map_list.remove(element)
                """
                if len(map_list) == 0:
                    return False # eller egen pos
                elif len(map_list) == 1:
                    return map_list[0] #
                """
                for species in cell.pop:
                    for animal in cell.pop[species]:
                        animal.migrate(cell, map_list)




                for cell in map_list:
                    cell.get_rel_abundance(animal)
                    cell.get_propensity(animal)
                total_propensity = sum([cell.propensity for cell in map_list])
                for cell in map_list:
                    cell.likelihood = cell.propensity / total_propensity




    """
            for species in self.map[pos].pop:
                copy = self.map[pos].pop[species]
                for animal in copy:
                    if animal.movable():
                        new_cell = self.choose_new_pos(pos, animal)
                        new_cell.pop[type(animal).__name__].append(animal)
                        self.map[pos].pop[type(animal).__name__].remove(animal)
                        new_cell.update_num_animals()
                        self.map[pos].update_num_animals()
    """

    """
    def choose_new_pos(self, position, animal):
        y, x = position
        list = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
        map_list = [self.map[element] for element in list]
        for cell in map_list:
            cell.get_rel_abundance(animal)
            cell.get_propensity(animal)
        total_propensity = sum([cell.propensity for cell in map_list])
        for cell in map_list:
            cell.likelihood = cell.propensity / total_propensity
        choices = np.random.choice(map_list, 1000, p=[cell.likelihood for cell
                                                      in map_list])
        # bør bruke random.random() og intervaller likevel
        chosen_cell = np.random.choice(choices)
        for candidate in map_list:
            candidate.rel_abundance = None
            candidate.propensity = None
        return chosen_cell
    """

    def update_num_animals(self):
        self.num_animals = 0
        self.num_animals_per_species = {'Herbivore': 0, 'Carnivore': 0}
        for cell in self.map.values(): # bør kunne flyttes inn
            self.num_animals += cell.num_animals
            for species in self.num_animals_per_species:
                self.num_animals_per_species[species] += cell.num_animals_per_species[species]

