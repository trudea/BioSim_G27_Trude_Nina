# -*- coding: utf-8 -*-

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

from math import exp
from .animals import Herbivore, Carnivore

class Landscape_cell:
    def __init__(self):
        self.f = 0
        self.num_animals = 0
        self.pop = []
        self.tot_w_herbivores = \
            sum([animal.weight for animal in self.pop if type(animal)
                 == Herbivore])
        self.num_animals = 0
        self.num_animals_per_species = {'Herbivore' : 0, 'Carnivore' : 0}
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
        for animal in self.pop:
            self.num_animals_per_species[type(animal).__name__] += 1
            self.num_animals += 1

    def replenish(self):
        pass

    def migration(self):
        moving = []
        for animal in self.pop:
            if animal.check_if_moves:
                new_cell = self.choose_new_cell(animal)
                moving.append({'loc': new_cell, 'pop': [{'species': type(animal).__name__, 'weight': animal.weight, 'age': animal.age}]})



class Savannah(Landscape_cell):
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


class Jungle(Landscape_cell):
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


class Desert(Landscape_cell):
    def __init__(self):
        super().__init__()
        self.f = 0


class Ocean(Landscape_cell):
    def __init__(self):
        super().__init__()


class Mountain(Landscape_cell):
    def __init__(self):
        super().__init__()
