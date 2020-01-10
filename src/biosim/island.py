# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"


# import animal.py
import numpy as np
from math import exp
import random


class Landscape:
    def __init__(self):
        pass

    def new_position(self):
        #when animal moves, this gives new position
        pass

    def growing(self):
        pass


class Savannah(Landscape):
    param_dict = {'f_max' : 300.0, 'alpha' : 0.3}

    def __init__(self, param_dict=None):
        super().__init__()
        self.herbivores_in_cell = []
        self.carnivores_in_cell = []
        if param_dict is not None:
            self.param_dict.update(param_dict)
        for parameter in self.param_dict:
            exec("self.%s = %s" % (parameter, self.param_dict[parameter]))
        self.f = self.f_max
        # self.herbivores_in_cell = [first_herbivores[0], first_herbivores[1]]

    def replenish(self):
        self.f += self.alpha * (self.f_max - self.f)



class Jungle(Landscape):
    param_dict = {'f_max' : 800.0}

    def __init__(self, param_dict=None):
        super().__init__()
        if param_dict is not None:
            self.param_dict.update(param_dict)
        for parameter in self.param_dict:
            exec("self.%s = %s" % (parameter, self.param_dict[parameter]))
        self.f = self.f_max

    def replenish(self):
        self.f = self.f_max


class Desert(Landscape):
    def __init__(self):
        super().__init__()
        self.f = 0


class Ocean(Landscape):
    def __init__(self):
        super().__init__()


class Mountain(Landscape):
    def __init__(self):
        super().__init__()


class Animal:
    parameters_set = False
    def __init__(self, attribute_dict):
        if not self.parameters_set:
            for parameter in self.param_dict:
                if parameter == 'lambda':
                    self.lambdah = self.param_dict['lambda']
                else:
                    exec("self.%s = %s" % (
                    parameter, self.param_dict[parameter]))
            self.parameters_set = True
        self.age = None
        self.weight = None
        if attribute_dict is not None:
            if 'weight' in attribute_dict:
                self.weight = attribute_dict['weight']
            if 'age' in attribute_dict:
                self.age = attribute_dict['age']
        if self.age is None:
            self.age = 0
        if self.weight is None:
            statistic_population = np.random.normal(self.param_dict['w_birth'],
                                            self.param_dict['sigma_birth'],
                                              1000) # lager ny statistisk populasjon for hver instance?
            self.weight = np.random.choice(statistic_population)
        q_plus = 1.0 / (1 + exp(self.param_dict['phi_age'] *
                                (self.age - self.param_dict['a_half'])))
        q_minus = 1.0 / (1 + exp(-self.param_dict['phi_weight'] *
                                 (self.weight - self.param_dict['w_half'])))
        self.phi = q_plus * q_minus
    """
        if not self.parameters_set:
            self.set_parameters()
    """
    """

    @classmethod
    def set_parameters(cls, params=None):
        for parameter in cls.param_dict:
            # self.w_birth = default_param_dict[]
            setattr(cls, parameter, cls.param_dict[parameter])

        cls.parameters_set = True

    """


    def aging(self):
        self.age += 1

    def gaining_weight(self, fodder):
        self.weight += (self.beta * fodder)

    def losing_weight(self):
        self.weight -= (self.eta * self.weight) #test en gang per år


    def check_if_dying(self):
        # returnerer om dyret skal dø eller ikke
        """else:
                   probability = round(self.param_dict['omega'] * (1 - self.phi), 3)
                   self.phi = random.choices([1, 0], [probability, 1 - probability])
                   if self.phi == 0:
                       '''død'''"""
        probability = round(self.param_dict['omega'] * (1 - self.phi), 3)
        if self.phi == 0 or round(random.random(), 3) >= probability:
                return True
        else:
            return False


class Herbivore(Animal):
    param_dict = {'w_birth': 8.0,
                  'sigma_birth': 1.5,
                  'beta': 0.9,
                  'eta': 0.05,
                  'a_half': 40.0,
                  'phi_age': 0.2,
                  'w_half': 10.0,
                  'phi_weight': 0.1,
                  'mu': 0.25,
                  'lambda': 1.0,
                  'gamma': 0.2,
                  'zeta': 3.5,
                  'xi': 1.2,
                  'omega': 0.4,
                  'F': 10.0
                  }

    def __init__(self, attribute_dict=None):
        super().__init__(attribute_dict)

    def weightgain_and_fodder_left(self, available_fodder):
        if available_fodder >= self.F:
            fodder_eaten = self.F
            remaining_fodder = available_fodder - self.F
        if available_fodder < self.F:
            fodder_eaten = available_fodder
            remaining_fodder = 0
        if fodder_eaten > 0:
            self.gaining_weight(fodder_eaten)
        return remaining_fodder

class Carnivore(Animal):
    param_dict = {'w_birth': 6.0,
                          'sigma_birth': 1.0,
                          'beta': 0.75,
                          'eta': 0.125,
                          'a_half': 60.0,
                          'phi_age': 0.4,
                          'w_half': 4.0,
                          'phi_weight': 0.4,
                          'mu': 0.4,
                          'lambda': 1.0,
                          'gamma': 0.8,
                          'zeta': 3.5,
                          'xi': 1.1,
                          'omega': 0.9,
                          'F': 50.0,
                          'DeltaPhiMax' : 10.0
                          }

    def __init__(self, attribute_dict=None):
        super().__init__(attribute_dict)

    def check_if_kills(self):
        pass


class Cell:
    land_dict = {'S': Savannah, 'J': Jungle, 'O': Ocean, 'M': Mountain,
                     'D': Desert}
    def __init__(self, y, x, letter):
        self.landscape = self.land_dict[letter]()
        self.y = y
        self.x = x
        self.herb_pop = [] # instances av Herbivore i celle
        self.carn_pop = [] # instances av Carnivore i celle

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
        for placement_dict in input_list:
                y, x = placement_dict['loc']
                for individual in placement_dict['pop']:
                    if individual['species'] == 'Herbivore':
                        self.map[y][x].herb_pop.append(Herbivore(individual))
                    elif individual['species'] == 'Carnivore':
                        self.map[y][x].carn_pop.append(Carnivore(individual))


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

    def one_cycle(self):
    #while(self.years_run < self.desired_years):
        for row in i.island:
            for cell in row:
                cell.landscape.replenish()
                # eating, first herbs, then carns
                cell.herb_pop = self.bubble_sort_animals(cell.herb_pop)
                for herbivore in cell.herb_pop:
                    cell.landscape.f = herbivore.weightgain_and_fodder_left()
                cell.carn_pop = self.bubble_sort_animals(cell.carn_pop)
                for carnivore in cell.carn_pop:
                    # cell.landscape.f = carnivore.weightgain_and_fodder_left()
                    pass
                # procreation
                # migration
                # aging
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
    print(run.island.map[3][4].herb_pop[1].weight)





















