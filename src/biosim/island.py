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

    def all_animals(self, myfunc):
        for cell in self.map.values():
            for species in cell.pop:
                for animal in cell.pop[species]:
                    getattr(animal, myfunc)()


    def place_animals(self, input_list):
        for placement_dict in input_list:
            pos = placement_dict['loc']
            for individual_dict in placement_dict['pop']:
                if individual_dict['species'] not in self.map[pos].pop:
                    self.map[pos].pop[individual_dict['species']] = []
                new_animal = eval(individual_dict['species'])(individual_dict)
                self.map[pos].pop[individual_dict['species']].append(new_animal)
                if individual_dict['species'] == 'Herbivore':
                    self.map[pos].tot_w_herbivores += new_animal.weight


    def migration(self): # husk filtering
        for pos in self.map:
            for species in self.map[pos].pop:
                copy = self.map[pos].pop[species]
                for animal in copy:
                    if animal.movable():  # endre navn slik at animal.moves?
                        new_cell = self.choose_new_pos(pos, animal)
                        new_cell.pop[type(animal).__name__].append(animal)
                        self.map[pos].pop[type(animal).__name__].remove(animal)

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


    def update_num_animals(self):
        self.num_animals = 0
        self.num_animals_per_species = {'Herbivore': 0, 'Carnivore': 0}
        for cell in self.map.values():
            cell.update_num_animals()
            self.num_animals += cell.num_animals
            for species in self.num_animals_per_species:
                self.num_animals_per_species[species] +=\
                    cell.num_animals_per_species[species]

    def feeding(self):
        for cell in self.map.values():
            for species in cell.pop:
                species = sorted(cell.pop[species], key=lambda x: getattr(x, 'phi'))
            for herbivore in cell.pop['Herbivore']:
                    cell.f = herbivore.weightgain_and_fodder_left(cell.f)
            for carnivore in cell.pop['Carnivore']:
                    eaten = 0
                    copy = cell.pop['Herbivore']
                    for prey in copy:  # use filtering
                        if eaten < carnivore.F:
                            if carnivore.check_if_kills(prey):
                                carnivore.gaining_weight(prey.weight)
                                carnivore.evaluate_fitness()
                                self.remove_animal(cell, prey)
                                self.num_animals -= 1
                                self.num_animals_per_species['Herbivore'] -= 1

    """
    def collective_procreation(self):
        # bør flyttes til celle?
        # species_dict = [Herbivore, Carnivore]
        for cell in self.map.values():
            cell.procreation()
    """

"""
    def aging(self):
        for cell in self.map.values():
            for species in cell.pop:
                for animal in cell.pop[species]:
                    animal.age += 1
"""
"""
    def weightloss(self):
        for cell in self.map.values():
            for species in cell.pop:
                for animal in cell.pop[species]:
                    animal.losing_weight()
"""