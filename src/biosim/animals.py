# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

import numpy as np
from math import exp
import random


class Animal:
    parameters_set = False

    """
    def evaluate_fitness(self):
        q_plus = 1.0 / (1 + exp(self.param_dict['phi_age'] *
                                (self.age - self.param_dict['a_half'])))

        q_minus = 1.0 / (1 + exp(-self.param_dict['phi_weight'] *
                                 (self.weight - self.param_dict['w_half'])))

        self.phi = q_plus * q_minus
    """

    def __init__(self, attribute_dict):

        if not self.parameters_set:
            for parameter in self.param_dict:
                if parameter == 'lambda':
                    self.lambdah = self.param_dict['lambda']
                else:
                    exec("self.%s = %s" % (parameter,
                                           self.param_dict[parameter]))
            self.parameters_set = True
        self.age = None
        self.weight = None
        # self.phi = None

        if attribute_dict is not None:
            if 'weight' in attribute_dict:
                self.weight = attribute_dict['weight']
            if 'age' in attribute_dict:
                self.age = attribute_dict['age']
            if 'phi' in attribute_dict:
                self.phi = attribute_dict['phi']

        if self.age is None:
            self.age = 0

        if self.weight is None:
            statistic_population = \
                np.random.normal(self.param_dict['w_birth'],
                                 self.param_dict['sigma_birth'], 1000)
            self.weight = np.random.choice(statistic_population)


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

    @property
    def phi(self):
        q_plus = 1.0 / (1 + exp(self.param_dict['phi_age'] *
                                (self.age - self.param_dict['a_half'])))

        q_minus = 1.0 / (1 + exp(-self.param_dict['phi_weight'] *
                                 (self.weight - self.param_dict[
                                     'w_half'])))

        return q_plus * q_minus

    def aging(self):
        self.age += 1

    def weightloss(self):
        if (self.eta * self.weight) <= self.weight:
            self.weight -= (self.eta * self.weight)
        elif (self.eta * self.weight) > self.weight:
            self.weight = 0

    def dies(self):
        probability = self.param_dict['omega'] * (1 - self.phi)
        if self.weight <= 0:
            return True
        elif self.phi <= 0:
            return True
        elif random.random() <= probability:
            return True
        else:
            return False

    def movable(self):
        probability = self.mu * self.phi
        if random.random() <= probability:
            return True
        else:
            return False

    def move(self, old_cell, new_cell):
        new_cell.pop[type(self).__name__].append(self)
        old_cell.pop[type(self).__name__].remove(self)

    def remove(self, cell):
        cell.pop[type(self).__name__].remove(self)

    def fertile(self, n):
        probability = self.lambdah * self.phi * (n-1)
        if probability > 1.0:
            probability = 1.0
        elif random.random() <= probability:
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

    def feeding(self, cell):
        if cell.f >= self.F:
            cell.f -= self.F
            m = self.weight
            self.weight += (self.beta * self.F)
            if m >= self.weight:
                print('weight not gained')



        elif cell.f < self.F:
            cell.f = 0
            self.weight += (self.beta * cell.f)

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
                  'DeltaPhiMax': 10.0
                  }

    def __init__(self, attribute_dict=None):
        super().__init__(attribute_dict)

    def check_if_kills(self, herbivore):
        if self.phi <= herbivore.phi:
            return False
        elif 0 < self.phi - herbivore.phi < 1.0:
            probability = (self.phi - herbivore.phi) / self.DeltaPhiMax
            if random.random() <= probability:
                return True
            else:
                return False

    def feeding(self, cell):
        eaten = 0
        dead = []
        for prey in cell.pop['Herbivore']:
            if eaten < self.F:
                if self.check_if_kills(prey):
                    x = self.weight
                    self.weight += self.beta * prey.weight
                    if self.weight <= x:
                        print('Carni weight not gained')
                    c = self.phi
                    if self.phi <= c and self.phi < 0.98:
                        # print(c, ' ', self.phi)
                        # print('Fitness not updated')
                        pass
                    dead.append(prey)
        cell.pop['Herbivore'] = [herbivore for herbivore in cell.pop['Herbivore'] if herbivore not in dead]


