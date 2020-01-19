# -*- coding: utf-8 -*-

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

import inspect
from math import exp
import numpy as np
from pytest import approx
import random
import src.biosim.animals as animals
from .animals import Herbivore, Carnivore


class LandscapeCell:
    def __init__(self):
        self.params_set = False
        self.f = 0
        self.species_to_class = dict(inspect.getmembers(animals, inspect.isclass))
        del self.species_to_class['Animal']
        self.pop = {'Herbivore': [], 'Carnivore': []}
        #self.tot_w_herbivores = \
        #    sum([herbivore.weight for herbivore in self.pop['Herbivore']])

    def num_specimen(self, species):
        return len(self.pop[species])

    """
    @property
    def num_animals_per_species(self):
        num_dict = {}
        for species in self.pop:
            num_dict[species] = len(self.pop[species])
        return num_dict
    """

    """
    @property
    def num_animals(self):
        total = 0
        for species in self.pop:
            total += len(self.pop[species])
        return total
    """

    @property
    def tot_w_herbivores(self):
        return sum([herbivore.weight for herbivore in self.pop['Herbivore']])

    @property
    def rel_abundance(self):
        return self._rel_abundance

    @rel_abundance.setter
    def rel_abundance(self, animal):
        fodder = 0
        if type(animal) == Herbivore:
            fodder = self.f
        elif type(animal) == Carnivore:

            fodder = self.tot_w_herbivores
        n = self.num_specimen(type(animal).__name__)

        self._rel_abundance = fodder / ((n + 1) * animal.F)


    @property
    def propensity(self):
        return self._propensity

    @propensity.setter
    def propensity(self, animal):
        if type(self) == Ocean:
            self._propensity = 0
        elif type(self) == Mountain:
            self._propensity = 0
        else:
            self.rel_abundance = animal
            self._propensity = exp(animal.lambdah * self._rel_abundance)

    @property
    def likelihood(self):
        return self._likelihood

    @likelihood.setter
    def likelihood(self, total):
        self._likelihood = self._propensity / total


    def migration(self, map_list):
        """
        Move each animal if the conditions require so.

        :param map_list: List of potential destinations for animal
        """
        for species in self.pop:
            for animal in self.pop[species]:
                if len(map_list) == 0:
                    pass
                elif len(map_list) == 1:
                    animal.move(self, map_list[0])
                else:
                    new_cell = self.new_cell(animal, map_list)
                    animal.move(self, new_cell)

    def new_cell(self, animal, map_list):
        """
        Find which cell the animal should move to, if it should move.

        :param animal: Instance of animal class
        :param map_list: List of potential destinations for animal
        :return: landscape instance. Either the cell the animal should move to,
         or the same cell if the animal shouldn't move.
        """
        for cell in map_list:
            cell.propensity = animal # setter verdi
        total_propensity = sum([cell.propensity for cell in map_list])
        for cell in map_list:
            cell.likelihood = total_propensity
        if not sum([cell.likelihood for cell in map_list]) == approx(1):
            print('Probabilities do not add up: ', sum([cell.likelihood for cell in map_list]))
        upper_limits = np.cumsum([cell.likelihood for cell in map_list])
        r = random.random()
        for i in range(len(upper_limits)):
            if r <= upper_limits[i]:
                return map_list[i]

    def place_animals(self, pop_list):
        """
        Place animals on a location.

        :param pop_list: List of dictionaries, each dictionary specifying
        characteristics of the individual animal to be placed.
        """
        for individual_dict in pop_list:
            if individual_dict['species'] not in self.pop:
                self.pop[individual_dict['species']] = []
            if individual_dict['age'] < 0:
                raise ValueError
            if individual_dict['weight'] <= 0:
                raise ValueError

            new_animal = eval(individual_dict['species'])(individual_dict)
            self.pop[individual_dict['species']].append(new_animal)

    def replenish(self):
        """Replenish plant fodder if required. """
        pass

    def feeding(self):
        """ Carry out feeding of each animal on the location. """
        for species in self.pop:
            self.pop[species] = sorted(self.pop[species], key=lambda x: getattr(x, 'phi'))
        for herbivore in self.pop['Herbivore']:
            herbivore.feeding(self)
        for carnivore in self.pop['Carnivore']:
            carnivore.feeding(self)

    def procreation(self):
        """Carry out procreation of animals on the location. """
        for species, pop_list in self.pop.items():
            copy = pop_list
            for animal in copy:
                n = self.num_specimen(species)
                if n >= 2:
                    if animal.fertile(n):
                        animal.procreate(self)


    def dying(self):
        """
        Remove dying animals from population
        """
        for species in self.pop:
            self.pop[species] = [animal for animal in self.pop[species] if not animal.dies()]

class Savannah(LandscapeCell):
    params = {'f_max': 300.0, 'alpha': 0.3}

    def __init__(self, new_params=None):
        super().__init__()
        if not self.params_set:
            self.set_params()
            self.params_set = True

        self.f = self.f_max


    @classmethod
    def set_params(cls, new_params=None):
        if new_params is not None:
            for param in new_params:
                if param not in cls.params:
                    raise ValueError
                if param == 'f_max' and new_params[param] < 0:
                    raise ValueError
            cls.params.update(new_params)
        for param in cls.params:
            setattr(cls, param, cls.params[param])
        cls.params_set = True

    def replenish(self):
        """Replenish plant fodder at the start of every season. """
        self.f = self.alpha * (self.f_max - self.f) + self.f


class Jungle(LandscapeCell):
    params = {'f_max': 800.0}

    def __init__(self, param_dict=None):
        super().__init__()
        if not self.params_set:
            self.set_params()

        self.f = self.f_max

    @classmethod
    def set_params(cls, new_params=None):
        if new_params is not None:
            for param in new_params:
                if param not in cls.params:
                    raise ValueError
                if param == 'f_max' and new_params[param] < 0:
                    raise ValueError
            cls.params.update(new_params)
        for param in cls.params:
            setattr(cls, param, cls.params[param])
        cls.params_set = True

    def replenish(self):
        """Replenish plant fodder at the start of every season. """
        self.f = self.f_max


class Desert(LandscapeCell):
    def __init__(self):
        super().__init__()
        self.f = 0


class Ocean(LandscapeCell):
    def __init__(self):
        super().__init__()


class Mountain(LandscapeCell):
    def __init__(self):
        super().__init__()
