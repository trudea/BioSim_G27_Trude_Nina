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


    def procreation(self):
        pass

    def migration(self):
        pass

class Run:
    def bubble_sort_animals(original_order):
        copy = list(original_order)
        for i in range(len(copy) - 1):
            for j in range(len(copy) - i - 1):
                if copy[j].phi < copy[j + 1].phi:
                    copy[j], copy[j + 1] = copy[j + 1], copy[j]
        return copy

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

    def num_of_species_in_cell(cell, species): # privat?
        n = 0
        for animal in cell.pop:
            if type(animal)==species:
                n+=1
        return n


    def collective_procreation(self):
        species_dict = [Herbivore, Carnivore]
        for row in self.island.map:
            for cell in row:
                for animal in cell.pop:
                    N = self.num_species_in_cell(cell, type(animal))
                    if N >= 2:
                        probability = animal.gamma * animal.phi * (N-1)
                        if probability > 1:
                            probability = 1
                        if round(random.random(), 3) <= probability:
                            return True




    def one_cycle(self):
        #while(self.years_run < self.desired_years):
        #bør deles opp i funksjoner
        self.collective_replenishing()
        self.collective_feeding()


        # procreation
        # migration
        # aging
        for animal in cell.pop:
            self.aging()
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




















