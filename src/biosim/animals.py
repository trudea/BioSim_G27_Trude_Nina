# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

import numpy as np
from math import exp
import random
import pytest


class Animal:
    """Create animals with weight and age, and have them perform actions like
    eating, losing weight and dying. """



    def __init__(self, attribute_dict):
        """
        :param attribute_dict: Dictionary specifying age and weight of animal
        """
        self.params_set = False
        self.age = None
        self.weight = None

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
                np.random.normal(self.params['w_birth'],
                                 self.params['sigma_birth'], 1000)
            self.weight = np.random.choice(statistic_population)

    @classmethod
    def set_params(cls, new_params=None):
        if new_params is not None:
            for param in new_params:
                if param not in cls.params:
                    raise ValueError
            cls.params.update(new_params)
        for param in cls.params:
            if param == 'lambda':
                cls.lambdah = cls.params['lambda']
            else:
                setattr(cls, param, cls.params[param])
        cls.params_set = True

    @property
    def phi(self):
        """
        Evaluate the fitness of an animal.

        :return: Float signifying level of fitness with a number between 0 and
        1.
        """

        q_plus = 1.0 / (1 + exp(self.params['phi_age'] *
                                (self.age - self.params['a_half'])))

        q_minus = 1.0 / (1 + exp(-self.params['phi_weight'] *
                                 (self.weight - self.params[
                                     'w_half'])))

        return q_plus * q_minus

    def aging(self):
        """ Make animal age by one year. """
        self.age += 1

    def weightloss(self):
        """ Execute annual weight loss for animal. """
        if (self.eta * self.weight) <= self.weight:
            self.weight -= (self.eta * self.weight)
        elif (self.eta * self.weight) > self.weight:
            self.weight = 0

    def dies(self):
        """
        Check if animal is dying.

        :return: Boolean value, True for dying and False for surviving.
        """
        probability = self.params['omega'] * (1 - self.phi)
        if self.weight <= 0:
            return True
        elif self.phi <= 0:
            return True
        elif np.random.random() <= probability:
            return True
        else:
            return False

    def movable(self):
        """
        Check if animal will move.

        :return: Boolean value, True for will move and False for will stay.
        """
        probability = self.mu * self.phi
        if np.random() <= probability:
            return True
        else:
            return False

    def migrate(self, current_cell, neighbours):
        if len(neighbours) == 0:
            return
        elif len(neighbours) == 1:
            new_cell = neighbours[0]
        else:
            new_cell = self.choose_new_cell(current_cell, neighbours)
            self.move(current_cell, new_cell)

    def choose_new_cell(self, current_cell, neighbours):
        """
        Find which cell the animal should move to, if it should move.

        :param animal: Instance of animal class
        :param map_list: List of potential destinations for animal
        :return: landscape instance. Either the cell the animal should move to,
         or the same cell if the animal shouldn't move.
        """
        for current_cell in neighbours:
            current_cell.propensity = self   # setter verdi
        total_propensity = sum([cell.propensity for cell in neighbours])
        for cell in neighbours:
            cell.likelihood = total_propensity
        """
        if not sum([cell.likelihood for cell in map_list]) == approx(1):
            print('Probabilities do not add up: ', sum([cell.likelihood for
                                                        cell in map_list]))
        """
        upper_limits = np.cumsum([cell.likelihood for cell in neighbours])
        r = np.random.random()
        for i in range(len(upper_limits)):
            if r <= upper_limits[i]:
                return neighbours[i]

    def move(self, old_cell, new_cell):
        """
        Move animal.

        :param old_cell: Landscape instance, the location of the animal before move
        :param new_cell: Landscape instance, the destination of the animal
        """

        new_cell.pop[type(self).__name__].append(self)
        old_cell.pop[type(self).__name__].remove(self)

    def fertile(self, n):
        """Check if animal is fertile.

        :return: Boolean value, True for fertile and False for infertile.
        """
        probability = self.lambdah * self.phi * (n-1)
        if probability > 1.0:
            probability = 1.0
        if np.random.random() <= probability:
            return True
        else:
            return False

    def procreate(self, cell):
        """ Animal gives birth to newborn if conditions are fulfilled.

         :param cell: Instance of landscape in which the animal is currently
         staying.
        """

        newborn = type(self)()
        if self.weight >= self.zeta * (
                newborn.weight + self.sigma_birth):

            cell.pop[type(self).__name__].append(newborn)
            self.weight -= self.zeta * newborn.weight
            if self.weight < 0:
                print('animal weight too small after birth')


class Herbivore(Animal):
    """Create an herbivore that can feed. """

    params = {'w_birth': 8.0,
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
        """

        :param attribute_dict: Dictionary specifying age and weight of animal.
        """
        super().__init__(attribute_dict)
        if not self.params_set:
            self.set_params()
            self.params_set = True

    def feeding(self, cell):
        """Carry out feeding of single herbivore.

        :param cell: Instance of landscape in which the animal is currently
         staying.
        """

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
    params = {'w_birth': 6.0,
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
        if not self.params_set:
            self.set_params()

    def check_if_kills(self, herbivore):
        if self.phi <= herbivore.phi:
            return False
        elif 0 < self.phi - herbivore.phi < 1.0:
            probability = (self.phi - herbivore.phi) / self.DeltaPhiMax
            if np.random.random() <= probability:
                return True
            else:
                return False

    def feeding(self, cell):
        """Carry out feeding of carnivore """
        eaten = 0
        dead = []
        for prey in cell.pop['Herbivore']:
            if eaten < self.F:
                if self.check_if_kills(prey):
                    self.weight += self.beta * prey.weight
                    dead.append(prey)
                    eaten += prey.weight
        cell.pop['Herbivore'] =\
            [herbivore for herbivore in cell.pop['Herbivore']
             if herbivore not in dead]
