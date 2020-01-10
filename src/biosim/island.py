# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"


# import animal.py
import numpy as np
from math import exp
import random


class Island:
    def __init__(self, txt=None):
        if txt is None:
            txt = open('rossum.txt').read()
            if txt[-1] == "\n":
                #legg inn noe som fjerner siste element
                print('geg')
                pass
        land_dict = {'S': Savannah, 'J': Jungle,
                     'O': Ocean, 'M': Mountain, 'D': Desert}
        line, lines = [], []
        x, y = 0, 0
        for letter in txt:
            if letter in land_dict:
                line.append(letter)
                x += 1
            if letter == "\n":
                lines.append(line)
                line = []
                y += 1
        lines.append(line)
        print(lines[-1])
        self.map = np.asarray(lines)







        """
        lines = []
        line = []
        y = 0
        x = 0

        for letter in txt:
            if letter in land_dict:
                # line.append(land_dict[letter](y, x))
                line.append(letter)
                x += 1
            elif letter == "\n":
                lines.append(line)
                line = []
                y += 1
                x = 0
            lines.append(line)
        print(lines)
        print(len(lines))
        self.map = np.asarray(lines)

        """
        """
        left_column = [line[0] for line in self.map]
        right_column = [line[-1] for line in self.map]
        to_check = [self.map[0], self.map[-1], left_column, right_column]
        for list in to_check:
            for element in list:
                if not isinstance(element, Ocean):
                    raise ValueError
        """

        """
        for letter in txt:
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
                n += 1
                y += 1
            x += 1
        """




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

    def __init__(self, pos_y, pos_x, param_dict=None):
        super().__init__()
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
    param_dict = {'f_max' : 800.0}

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
    parameters_set = False
    def __init__(self, island, attribute_dict):
        self.island = island
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
    def feeding(self, fodder):
        self.weight += (self.beta * fodder)


    def procreation(self):
        pass

    def migration(self):
        pass

    def aging(self):
        self.age += 1

    def weightloss(self):
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

    def __init__(self, island, attribute_dict=None):
        super().__init__(island, attribute_dict)

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

    def __init__(self, island, attribute_dict=None):
        super().__init__(island, attribute_dict)

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
                if location['pop'][n]['species'] == 'Carnivore':
                    temp_dict = {}
                    temp_dict['age'] = location['pop'][n]['age']
                    temp_dict['weight'] = location['pop'][n]['weight']
                    herman = Carnivore(island_map, temp_dict, y, x)
                    island_map[y][x].carnivores_in_cell.append(herman)
        return map

    def single_run(self):
       pass


if __name__ == "__main__":
    """
    first_island = Island()
    map = first_island.map
    """
    """
    initial_num_of_herbivores = 3
    initial_num_of_carnivores = 2
    current_herbivores = []
    current_carnivores = []
    """
    """
    for _ in range(initial_num_of_herbivores):
        current_herbivores.append(Herbivore(map))  # legger ny instance til liste
    for _ in range(initial_num_of_carnivores):
        current_carnivores.append(Carnivore(first_island))
"""
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
                if location['pop'][n]['species'] == 'Carnivore':
                    temp_dict = {}
                    temp_dict['age'] = location['pop'][n]['age']
                    temp_dict['weight'] = location['pop'][n]['weight']
                    herman = Carnivore(island_map, temp_dict, y, x)
                    island_map[y][x].carnivores_in_cell.append(herman)
        return map

    def move_animal(the_animal, new_x, new_y):
        # the_animal = map[y][x].carnivores_in_cell[n]
        previous_x = the_animal.pos_x
        previous_y = the_animal.pos_y

    # map = place_animals(default_input, map)

    c = Carnivore(map, {'age':99})
    h = Herbivore(map)
    simple_string = 'SOO\nOOO'
    simple_island = Island()





















