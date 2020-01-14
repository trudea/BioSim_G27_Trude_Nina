# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

import numpy as np
from .landscapes import Savannah, Jungle, Ocean, Mountain, Desert
from .animals import Herbivore, Carnivore


class Island:
    # ta høyde for store og små bokstaver
    land_dict = {'S': Savannah, 'J': Jungle,
                 'O': Ocean, 'M': Mountain, 'D': Desert}

    def str_to_dict(self, txt):
        # burde ha check_edges som en egen funksjon?
        txt = txt.split('\n')
        if txt[-1] == '\n':
            txt = txt.pop()
        # print(type(txt))
        # print(txt[-1])
        edges = txt[0] + txt[-1]
        #print((edges))
        #edges.append(txt[])
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
                self.map[pos].tot_w_herbivores += new_animal.weight

    def remove_animal(self, cell, animal):
        cell.pop.remove(animal)
    """
    def move_animal(self, old_cell, new_cell, animal):
        new_cell.pop.append(animal)
        old_cell.pop.remove(animal)  # use filtering?
    """
    def migration(self):
        copy = self.map
        for pos in copy:
            for animal in copy[pos].pop:
                if animal.check_if_moves:  # endre navn slik at animal.moves?
                    new_cell = self.choose_new_pos(pos, animal)
                    new_cell.pop.append(animal)
                    self.map[pos].pop.remove(animal)

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
            cell.pop = sorted(cell.pop, key=lambda x: getattr(x, 'phi'))
            for animal in cell.pop:
                if type(animal) == Herbivore:
                    cell.f = \
                        animal.weightgain_and_fodder_left(cell.f)

            for animal in cell.pop:
                if type(animal) == Carnivore:
                    eaten = 0
                    copy = cell.pop
                    for other_animal in copy:  # use filtering
                        if eaten < animal.F and type(
                                other_animal) == Herbivore:
                            if animal.check_if_kills(other_animal):
                                animal.gaining_weight(
                                    other_animal.weight)
                                animal.evaluate_fitness()
                                self.remove_animal(cell,
                                                   other_animal)

    def collective_procreation(self):
        # bør flyttes til celle?
        # species_dict = [Herbivore, Carnivore]
        for cell in self.map.values():
            cell.procreation()


    def aging(self):
        for cell in self.map.values():
            for animal in cell.pop:
                animal.age += 1

    def weightloss(self):
        for cell in self.map.values():
            for animal in cell.pop:
                animal.losing_weight()

    def dying(self):
        for cell in self.map.values():
            for animal in cell.pop:
                if animal.check_if_dying():
                    self.remove_animal(cell, animal)
