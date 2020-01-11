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
from island import Island, Cell

class Run:
    default_input = [{'loc': (3, 4), 'pop': [
        {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
        {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
        {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]},
                     {'loc': (4, 4),
                      'pop': [
                          {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
                          {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
                          {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]}]

    def __init__(self, desired_years=10, input=None):
        self.desired_years = desired_years
        self.years_run = 0
        if input is None:
            input = default_input
        self.island = Island()
        self.island.place_animals(input)

    def collective_replenishing(self):
        for row in self.island.map:
            for cell in row:
                if type(cell) == Savannah or type(cell) == Jungle:
                    cell.landscape.replenish()

    def collective_feeding(self):
        active = [Savannah, Jungle, Desert]
        for row in self.island.map:
            for cell in row:
                if type(cell) in active and len(cell.pop) > 0:
                    cell.pop = self.bubble_sort_animals(cell.pop)  # sorterer alle
                    # dyrene etter fitness, men bare å passe på at vi velger ut et species når vi kaller
                    for animal in cell.pop:
                        if type(animal) == Herbivore:
                            cell.landscape.f = animal.weightgain_and_fodder_left()
                    for animal in cell.pop:
                        if type(animal) == Carnivore:
                            eaten = 0
                            for other_animal in cell.pop:
                                # unngår while for at ikke skal gjentas selv om carn ikke mett
                                if eaten < animal.F and type(
                                        other_animal) == Herbivore:
                                    if animal.check_if_kills(other_animal):
                                        animal.gaining_weight(other_animal.weight)
                                        animal.evaluate_fitness()
                                        self.remove_animal(cell, other_animal)




    def collective_procreation(self):
        species_dict = [Herbivore, Carnivore]
        for row in self.island.map:
            for cell in row:
                N_dict = {Herbivore:
                              Island.num_specimen_in_cell(cell, Herbivore),
                          Carnivore: Island.num_specimen_in_cell(cell, Carnivore)}
                for animal in cell.pop:
                    N = N_dict[type(animal)]
                    print(N)
                    if N >= 2:
                            if animal.check_if_procreates(N):
                                newborn = cell.pop.append(type(animal)())
                                if newborn.weight < animal.weight:
                                    cell.pop.append(newborn)
                                    animal.weight -= animal.zeta * newborn.weight


    def collective_migration(self):
        for row in self.island.map:
            for cell in row:
                for animal in cell.pop:
                    # check for each adjecent cell if animal would move there,tar inn self.island
                    pass

    def collective_aging(self):
        for row in self.island.map:
            for cell in row:
                for animal in cell.pop:
                    animal.aging()


    def one_cycle(self):
        #while(self.years_run < self.desired_years):
        #bør deles opp i funksjoner
        self.collective_replenishing()
        self.collective_feeding()
        # procreation
        self.collective_procreation()
        # migration
        self.collective_migration()
        # aging
        self.collective_aging()
        # weightloss
        # death

if __name__ == "__main__":
    default_input = [{'loc': (3, 4), 'pop': [
        {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
        {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
        {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]},
                     {'loc': (4, 4),
                      'pop': [
                          {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
                          {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
                          {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]}]

    #i = Island()
    #i.place_animals(default_input)

    run = Run()
    run.one_cycle()
    for animal in run.island.map[3][4].pop:
        # print(type(animal))
        if type(animal) == Herbivore:
            # print(True)
            pass
    pop = default_input[0]['pop']




















