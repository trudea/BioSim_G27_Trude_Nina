# -*- coding: utf-8 -*-

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

import inspect
from math import exp
import src.biosim.animals as animals
from .animals import Herbivore, Carnivore


class LandscapeCell:
    def __init__(self):
        self.f = 0
        self.num_animals = 0
        self.species_to_class = dict(
            inspect.getmembers(animals, inspect.isclass))
        del self.species_to_class['Animal']
        self.pop = {}
        """
        for species in self.species_to_class.keys():
            print(species)
            self.pop = {species: []}
        """
        self.pop = {'Herbivore': [], 'Carnivore': []}
        self.tot_w_herbivores = \
            sum([animal.weight for animal in self.pop if type(animal)
                 == Herbivore])
        self.num_animals = 0
        self.num_animals_per_species = {'Herbivore': 0, 'Carnivore': 0}
        self.rel_abundance = None
        self.propensity = None
        self.likelihood = None

    def num_specimen(self, species):
        n = 0
        for animal in self.pop:
            if type(animal) == species:
                n += 1
        return n

    def get_rel_abundance(self, animal):
        if type(animal) == Herbivore:
            fodder = self.f

        if type(animal) == Carnivore:
            fodder = self.tot_w_herbivores

        n = self.num_specimen(type(animal))
        self.rel_abundance = fodder / ((n + 1) * animal.F)

    def get_propensity(self, animal):
        if type(self) == Ocean:
            self.propensity = 0
        elif type(self) == Mountain:
            self.propensity = 0
        else:
            self.propensity = exp(animal.lambdah * self.rel_abundance)

    def update_num_animals(self):
        for species in self.pop:
            for animal in self.pop[species]:
                self.num_animals_per_species[type(animal).__name__] += 1
                self.num_animals += 1

    def replenish(self):
        pass

    def migration(self):
        moving = []
        for animal in self.pop:
            if animal.check_if_moves:
                new_cell = self.choose_new_cell(animal)
                moving.append({'loc': new_cell, 'pop': \
                    [{'species': type(animal).__name__,
                      'weight': animal.weight, 'age': animal.age}]})

    def procreation(self):
        N_dict = {Herbivore: self.num_specimen(Herbivore),
                  Carnivore: self.num_specimen(Carnivore)}
        newborns = 0
        for species in self.pop.keys():
            copy = self.pop[species]
            for animal in copy:
                # print(type(animal))
                n = N_dict[type(animal)]
                if n >= 2:
                    if animal.check_if_procreates(n):
                        newborn = type(animal)()
                        if newborn.weight < animal.weight:
                            self.pop.append(newborn)
                            animal.weight -= animal.zeta * newborn.weight
                            newborns += 1
            return newborns







    def remove_animal(self, animal):
        self.pop[type(animal).__name__].remove(animal)

    def dying(self):
        for species in self.pop:
            for animal in self.pop[species]:
                if animal.dies():
                    self.remove_animal(animal)
                    self.num_animals -= 1
                    self.num_animals_per_species[type(animal).__name__] -= 1

"""
    def weightloss(self):
        for species in self.pop:
            for animal in self.pop[species]:
                animal.losing_weight()
"""
class Savannah(LandscapeCell):
    param_dict = {'f_max': 300.0, 'alpha': 0.3}

    def __init__(self, param_dict=None):
        super().__init__()
        if param_dict is not None:
            self.param_dict.update(param_dict)
        for parameter in self.param_dict:
            exec("self.%s = %s" % (parameter, self.param_dict[parameter]))
        self.f = self.f_max

    def replenish(self):
        self.f = self.alpha * (self.f_max - self.f) + self.f


class Jungle(LandscapeCell):
    param_dict = {'f_max': 800.0}

    def __init__(self, param_dict=None):
        super().__init__()
        if param_dict is not None:
            self.param_dict.update(param_dict)
        for parameter in self.param_dict:
            exec("self.%s = %s" % (parameter, self.param_dict[parameter]))
        self.f = self.f_max

    def replenish(self):
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
