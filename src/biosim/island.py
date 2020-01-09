# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

import numpy as np
from math import exp
import random

class Landscape:

    def num_to_coord(self, cols, num):
        x, y = 0, 0
        while num > cols:
            y += 1
            num -= cols
        x = num
        return (y, x) # y før x

    def coord_to_num(self, cols, y, x): # y før x
        return y*cols + x


    def __init__(self, txt_str=None):
        if txt_str is None:
            txt_str = open('rossum.txt').read()
            # txt_str = txt_str.split() # liste med tekststrenger
            for i in txt_str[0]:
                if i != 'O':
                    raise ValueError
            map_str = txt_str.replace("\n", "") #  en lang streng
        self.map_string = map_str
        self.map_dict = {} # hver key er tuple av posisjonen, y før x
        self.cols = 21 # må endres
        for n, i in enumerate(self.map_string):
            self.map_dict[self.num_to_coord(self.cols, n)] = [i]


    def new_position(self):
        #when animal moves, this gives new position
        pass

    def growing(self):
        pass

class Savannah(Landscape):
    default_param_dict = {'f_max' : 300.0}
    savannah = []
    savannah_dict = {}

    def __init__(self, map_string, param_dict=None):
        self.map_string = map_string
        for n, i in enumerate(self.map_string):
            if i == 'S':
                self.coords.append(n)
                savannah_dict[(num_to_coords(n))] = 0
        if param_dict is None: # burde sannsynligvis være i superklassen
            self.param_dict = default_param_dict
        else:
            for i in default_param_dict:
                if i not in param_dict:
                    param_dict[i] = default_param_dict[i]


class Jungle(Landscape):
    default_param_dict = {'f_max' : 800.0, 'alpha' : 0.3}

    def __init__(self, island, param_dict):
        self.island = island
        if param_dict is None:
            self.param_dict = default_param_dict
        else:
            for i in default_param_dict:
                if i not in param_dict:
                    param_dict[i] = default_param_dict[i]


class Animal:
    def __init__(self, island, param_dict):
        self.phi = None
        self.param_dict = param_dict
        self.island = island
        self.age = 0


        self.position = 0 # må endres



    def feeding(self):

        pass

    def procreation(self):
        pass

    def migration(self):
        pass

    def aging(self):
        self.age += 1
        pass

    def weightloss(self):
        pass

    def dying(self):
        if self.phi == 0:
            """Fjern fra dyrelista/populasjonen, valueerror under 0"""
            return 1              # Sannsynlighet for død
        """else:
            probability = round(self.param_dict['omega'] * (1 - self.phi), 3)
            self.phi = random.choices([1, 0], [probability, 1 - probability])
            if self.phi == 0:
                '''død'''"""

        # random.random() genererer random floating point
        else:
            probability = round(self.param_dict['omega'] * (1 - self.phi), 3)
            if round(random.random(), 3) >= probability:
                # dyret dør


class Herbivore(Animal):
    default_param_dict = {'w_birth': 8.0,
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

    def __init__(self, island, param_dict=None):
        super().__init__(island)
        if param_dict is None:
            self.param_dict = self.default_param_dict
        else:
            for i in self.default_param_dict:
                if i not in param_dict:
                    param_dict[i] = self.default_param_dict[i]
                self.param_dict = param_dict
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
    default_param_dict = {'w_birth': 6.0,
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

    def __init__(self, island, param_dict=None):
        super().__init__(island)
        if param_dict is None:
            self.param_dict = self.default_param_dict
        else:
            for i in self.default_param_dict:
                if i not in param_dict:
                    param_dict[i] = self.default_param_dict[i]
                self.param_dict = param_dict
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
    first_herbivores = []
    first_carnivores = []
    for _ in range(initial_num_of_herbivores):
        first_herbivores.append(Herbivore(first_island))  # legger ny instance til liste
    for _ in range(initial_num_of_carnivores):
        first_carnivores.append(Carnivore(first_island))


