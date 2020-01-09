# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

import numpy as np
from math import exp
import random

class Island:
    def __init__(self, txt=None):
        if txt is None:
            txt = open('rossum.txt').read()
            for i in txt[0]:
                if i != 'O':
                    raise ValueError
        lines = []
        line = []
        y = 0
        x = -1
        for letter in txt:
            x += 1
            if letter == 'S':
                line.append(Savannah(y, x))
            if letter == 'J':
                line.append(Jungle(y, x))
            if letter == 'O':
                line.append(Ocean(y, x))
            if letter == 'M':
                line.append(Mountain(y, x))
            if letter == 'D':
                line.append(Desert(y, x))
            if letter == '\n':
                lines.append(line)
                line = []
                y +=1
                x = -1
        self.map = np.asarray(lines)


class Landscape:
    def __init__(self):
        pass

    def new_position(self):
        #when animal moves, this gives new position
        pass

    def growing(self):
        pass


class Savannah(Landscape):
    param_dict = {'f_max' : 300.0}

    def __init__(self, pos_y, pos_x, param_dict=None):
        self.herbivores_in_cell = []
        self.carnivores_in_cell = []
        self.pos_y = pos_y
        self.pos_x = pos_x
        if param_dict is not None:
            self.param_dict.update(param_dict)
        for parameter in self.param_dict:
            exec("self.%s = %s" % (parameter, self.param_dict[parameter]))
        self.f = self.f_max
        # self.herbivores_in_cell = [first_herbivores[0], first_herbivores[1]]

    def replenish(self):
        self.f += self.alpha * (self.f_max - self.f)



class Jungle(Landscape):
    param_dict = {'f_max' : 800.0, 'alpha' : 0.3}

    def __init__(self, pos_y, pos_x, param_dict=None):
        self.herbivores_in_cell = []
        self.carnivores_in_cell = []
        self.pos_y = pos_y
        self.pos_x = pos_x
        if param_dict is not None:
            self.param_dict.update(param_dict)
        for parameter in self.param_dict:
            exec("self.%s = %s" % (parameter, self.param_dict[parameter]))
        self.f = self.f_max

    def replenish(self):
        self.f = self.f_max

class Desert:
    def __init__(self, pos_y, pos_x):
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.herbivores_in_cell = []
        self.carnivores_in_cell = []

class Ocean:
    def __init__(self, pos_y, pos_x):
        self.pos_y = pos_y
        self.pos_x = pos_x

class Mountain:
    def __init__(self, pos_y, pos_x):
        self.pos_y = pos_y
        self.pos_x = pos_x


class Animal:

    def __init__(self, island):
        # self.phi = None
        self.island = island
        self.age = None
        self.weight = None
        self.pos_y = None
        self.pos_x = None # må endres, midlertidig
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
    def feeding(self, fodder):
        self.weight + (self.beta * fodder)


    def procreation(self):
        pass

    def migration(self):
        pass

    def aging(self):
        self.age += 1

    def weightloss(self):
        self.weight - (self.eta * self.weight ) #test en gang per år


    def dying(self):
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
    # parameters_set = False
    param_dict = {'w_birth': 8.0,
                  'sigma_birth': 1.5,
                  'beta': 0.9,
                  'eta': 0.05,
                  'a_half': 40.0,
                  'phi_age': 0.2,
                  'w_half': 10.0,
                  'phi_weight': 0.1,
                  'mu': 0.25,
                  'lambdah': 1.0,
                  'gamma': 0.2,
                  'zeta': 3.5,
                  'xi': 1.2,
                  'omega': 0.4,
                  'F': 10.0
                  }

    def __init__(self, island, attribute_dict=None, pos_y=None, pos_x=None):
        super().__init__(island)
        if attribute_dict is not None:
            if 'weight' in attribute_dict:
                self.weight = attribute_dict['weight']
            if 'weight' in attribute_dict:
                self.age = attribute_dict['age']
                """
        if attribute_dict is not None:
            for parameter in self.param_dict:
                exec("self.%s = %s" % (parameter, self.param_dict[parameter]))
                """
        if self.age is None:
            self.age = 0
        if self.weight is None:
            statistic_population = np.random.normal(self.param_dict['w_birth'],
                                            self.param_dict['sigma_birth'],
                                              1000) # lager ny statistisk populasjon for hver instance?
            self.weight = np.random.choice(statistic_population)
        self.pos_y = pos_y
        self.pos_x = pos_x
        q_plus = 1.0 / (1 + exp(self.param_dict['phi_age'] *
                                (self.age - self.param_dict['a_half'])))
        q_minus = 1.0 / (1 + exp(-self.param_dict['phi_weight'] *
                                 (self.weight - self.param_dict['w_half'])))
        self.phi = q_plus * q_minus


class Carnivore(Animal):
    parameters_set = False
    param_dict = {'w_birth': 6.0,
                          'sigma_birth': 1.0,
                          'beta': 0.75,
                          'eta': 0.125,
                          'a_half': 60.0,
                          'phi_age': 0.4,
                          'w_half': 4.0,
                          'phi_weight': 0.4,
                          'mu': 0.4,
                          'lambdah': 1.0,
                          'gamma': 0.8,
                          'zeta': 3.5,
                          'xi': 1.1,
                          'omega': 0.9,
                          'F': 50.0,
                          'DeltaPhiMax' : 10.0
                          }

    def __init__(self, island, attribute_dict=None, pos_y=None, pos_x=None):
        super().__init__(island)
        if attribute_dict is not None:
            if 'weight' in attribute_dict:
                self.weight = attribute_dict['weight']
            if 'age' in attribute_dict:
                self.age = attribute_dict['age']
        if self.age is None:
                self.age = 0
        if self.weight is None:
            statistic_population = np.random.normal(
                self.param_dict['w_birth'],
                self.param_dict['sigma_birth'],
                1000)  # lager ny statistisk populasjon for hver instance?
            self.weight = np.random.choice(statistic_population)
        self.pos_y = pos_y
        self.pos_x = pos_x




    def check_if_kills(self):
        pass

class Simulation:
    default_input = [{'loc': (3,4), 'pop' : [{'species': 'Herbivore', 'age' : 10, 'weight' : 12.5},
                                      {'species': 'Herbivore', 'age' : 9, 'weight' : 10.3},
                                      {'species': 'Carnivore', 'age' : 5, 'weight' : 8.1}]},
             {'loc': (4, 4),
              'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
                      {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
                      {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]}]


    def __init__(self):
        pass


    def single_run(self):
       pass


if __name__ == "__main__":
    first_island = Island()
    map = first_island.map
    initial_num_of_herbivores = 3
    initial_num_of_carnivores = 2
    current_herbivores = []
    current_carnivores = []
    for _ in range(initial_num_of_herbivores):
        pass
        # current_herbivores.append(Herbivore(map))  # legger ny instance til liste
    for _ in range(initial_num_of_carnivores):
        current_carnivores.append(Carnivore(first_island))

    default_input = [{'loc': (3, 4), 'pop': [
        {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
        {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
        {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]},
                     {'loc': (4, 4),
                      'pop': [
                          {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
                          {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
                          {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]}]
    test_input = {'loc': (3, 4), 'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]}


    def place_animals(input, island_map):
        # tar for seg et og et koordinat (på dict-form) og plasserer et dyr av gangen i koordinatet
        for location in input:
            y, x = location['loc']
            for n, animal in enumerate(location['pop']):
                if location['pop'][n]['species'] == 'Herbivore':
                    temp_dict = {}
                    temp_dict['age'] = location['pop'][n]['age']
                    temp_dict['weight'] = location['pop'][n]['weight']
                    herman = Herbivore(island_map, temp_dict, y, x)
                    island_map[y][x].herbivores_in_cell.append(herman)
                    #print(map[3][4].herbivores_in_cell[n].age)
                if location['pop'][n]['species'] == 'Carnivore':
                    temp_dict = {}
                    temp_dict['age'] = location['pop'][n]['age']
                    temp_dict['weight'] = location['pop'][n]['weight']
                    herman = Carnivore(island_map, temp_dict, y, x)
                    island_map[y][x].carnivores_in_cell.append(herman)
                    # print(island_map[y][x].carnivores_in_cell[0])
        return map

    map = place_animals(default_input, map)
    print(map[3][4].carnivores_in_cell[0].weight)
    # print(map[3][4].herbivores_in_cell[1].age)






    def place_animal(individual_dict, island_map):
        # plassere i riktig celle, fjerne gammel celle og oppdatere posisjonen i dyre-instansen
        y, x = individual_dict['loc']
        age = individual_dict['pop'][0]['age']
        weight = individual_dict['pop'][0]['weight']
        if individual_dict['pop'][0]['species'] == 'Herbivore':
            del individual_dict['pop'][0]['species']
            herman = Herbivore(island_map, individual_dict['pop'][0], y, x)
            island_map[y][x].herbivores_in_cell.append(herman)





