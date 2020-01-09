# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

import numpy as np
from math import exp
import random

class Landscape:

    def __init__(self, txt=None):
        if txt is None:
            txt = open('rossum.txt').read()
            for i in txt[0]:
                if i != 'O':
                    raise ValueError
        map = []
        lines = []
        line = []
        for letter in txt:
            if letter == 'S':
                line.append(Savannah())
            if letter == 'J':
                line.append(Jungle())
            if letter == 'O':
                line.append(Ocean())
            if letter == 'M':
                line.append(Mountain())
            if letter == 'D':
                line.append(Desert())
            if letter == '\n':
                lines.append(line)
                line = []
        map = np.asarray(lines)
        print(len(map[0]))
        print(map[1][1].f_max)


        new_map = np.array(map)
        for y in new_map:
            for x in y:
                if x == '\n':
                    pass
                if x == 'S':
                    x = Savannah()
        self.map = new_map




    def new_position(self):
        #when animal moves, this gives new position
        pass

    def growing(self):
        pass

class Savannah(Landscape):
    param_dict = {'f_max' : 300.0}
    savannah = []
    savannah_dict = {}
    f_max = 5

    def __init__(self, param_dict=None):
        if param_dict is None: # burde sannsynligvis være i superklassen
            self.param_dict = param_dict
        else:
            for i in param_dict:
                if i not in param_dict:
                    param_dict[i] = param_dict[i]



class Jungle(Landscape):
    default_param_dict = {'f_max' : 800.0, 'alpha' : 0.3}

    def __init__(self, param_dict=None):
        pass
        """
        if param_dict is None:
            self.param_dict = default_param_dict
        else:
            for i in default_param_dict:
                if i not in param_dict:
                    param_dict[i] = default_param_dict[i]
"""
class Ocean:
    pass

class Mountain:
    pass

class Desert:
    pass


class Animal:

    def __init__(self, island):
        # self.phi = None
        self.island = island
        self.age = 0
        self.position = 0 # må endres, midlertidig

        # if not self.parameters_set:
        #    self.set_parameters()

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

    def __init__(self, island, param_dict=None):
        super().__init__(island)
        if param_dict is not None:
            self.param_dict.update(param_dict)
        for parameter in self.param_dict:
            exec("self.%s = %s" % (parameter, self.param_dict[parameter]))
        statistic_population = np.random.normal(self.param_dict['w_birth'],
                                            self.param_dict['sigma_birth'],
                                              1000)
        self.weight = np.random.choice(statistic_population)
        q_plus = 1.0 / (1 + exp(self.param_dict['phi_age'] *
                                (self.age - self.param_dict['a_half'])))
        q_minus = 1.0 / (1 + exp(-self.param_dict['phi_weight'] *
                                 (self.weight - self.param_dict['w_half'])))
        self.phi = q_plus * q_minus


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
                          'lambdah': 1.0,
                          'gamma': 0.8,
                          'zeta': 3.5,
                          'xi': 1.1,
                          'omega': 0.9,
                          'F': 50.0,
                          'DeltaPhiMax' : 10.0
                          }

    def __init__(self, island, param_dict=None):
        super().__init__(island)
        super().__init__(island)
        if param_dict is not None:
            self.param_dict.update(param_dict)
        for parameter in self.param_dict:
            exec("self.%s = %s" % (parameter, self.param_dict[parameter]))

        statistic_population = np.random.normal(self.param_dict['w_birth'],
                                            self.param_dict['sigma_birth'],
                                            1000)
        self.weight = np.random.choice(statistic_population)


    def check_if_kills(self):
        pass

class Simulation:
    def __init__(self):
        pass

    def single_run(self):
       pass

if __name__ == "__main__":
    initial_num_of_herbivores = 3
    initial_num_of_carnivores = 2
    first_island = Landscape()
    map = first_island.map
    first_herbivores = []
    first_carnivores = []
    for _ in range(initial_num_of_herbivores):
        first_herbivores.append(Herbivore(map))  # legger ny instance til liste

    for _ in range(initial_num_of_carnivores):
        first_carnivores.append(Carnivore(first_island))

    first_herbivores[0].phi = 0
    first_herbivores[0].dying()
    herb_dict = {'w_birth' : 33}
    herbert = Herbivore(first_island, herb_dict)

    carn_dict = {'sigma_birth' : 10, 'w_birth' : 3}
    new_dict = {'sigma_birth' : 2}
    carl = Carnivore(first_island, carn_dict)
    cole = Carnivore(first_island, new_dict)



