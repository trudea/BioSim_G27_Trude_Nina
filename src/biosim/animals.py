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

    def evaluate_fitness(self):
        q_plus = 1.0 / (1 + exp(self.param_dict['phi_age'] *
                                (self.age - self.param_dict['a_half'])))

        q_minus = 1.0 / (1 + exp(-self.param_dict['phi_weight'] *
                                 (self.weight - self.param_dict['w_half'])))

        self.phi = q_plus * q_minus

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

        if attribute_dict is not None:
            if 'weight' in attribute_dict:
                self.weight = attribute_dict['weight']
            if 'age' in attribute_dict:
                self.age = attribute_dict['age']

        if self.age is None:
            self.age = 0

        if self.weight is None:
            statistic_population = \
                np.random.normal(self.param_dict['w_birth'],
                                 self.param_dict['sigma_birth'], 1000)
            self.weight = np.random.choice(statistic_population)
        self.evaluate_fitness()

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
        self.evaluate_fitness()

    def gaining_weight(self, intake_weight):
        self.weight += (self.beta * intake_weight)
        self.evaluate_fitness()

    def losing_weight(self):
        self.weight -= (self.eta * self.weight)
        self.evaluate_fitness()

    def check_if_dying(self):
        probability = round(self.param_dict['omega'] * (1 - self.phi), 3)
        if self.phi == 0 or round(random.random(), 3) <= probability:
            return True
        else:
            return False

    def check_if_procreates(self, n):
        if self.age == 0:
            return False
        if self.weight < self.zeta * (self.w_birth + self.sigma_birth):
            return False
        probability = self.gamma * self.phi * (n - 1)
        if probability > 1:
            probability = 1
        if random.random() <= probability:
            return True
        else:
            return False

    def movable(self):
        probability = self.mu * self.phi
        if random.random() <= probability:
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
                  'DeltaPhiMax': 10.0
                  }

    def __init__(self, attribute_dict=None):
        super().__init__(attribute_dict)

    def check_if_kills(self, herbivore):
        if self.phi < herbivore.phi:
            return False
        elif 0 < self.phi - herbivore.phi < 1:
            probability = (self.phi - herbivore.phi) / self.DeltaPhiMax
            if round(random.random(), 7) <= probability:
                return True
            else:
                return False
        else:
            return False
