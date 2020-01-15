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
        # self.num_animals = 0
        self.species_to_class = dict(inspect.getmembers(animals, inspect.isclass))
        del self.species_to_class['Animal']
        self.pop = {'Herbivore': [], 'Carnivore': []}
        self.tot_w_herbivores = \
            sum([herbivore.weight for herbivore in self.pop['Herbivore']])
        # self.num_animals_per_species = {'Herbivore': 0, 'Carnivore': 0}
        self.rel_abundance = None
        self.propensity = None
        self.likelihood = None

    def num_specimen(self, species):
        return len(self.pop[species])

    def num_animals_per_species(self):
        num_dict = {}
        for species in self.pop:
            num_dict[species] = len(self.pop[species])
        return num_dict

    def num_animals(self):
        total = 0
        for species in self.pop:
            total += len(self.pop[species])
        return total

    def get_rel_abundance(self, animal):
        if type(animal) == Herbivore:
            fodder = self.f

        if type(animal) == Carnivore:
            fodder = self.tot_w_herbivores

        n = (self.pop[type(animal).__name__])
        self.rel_abundance = fodder / ((n + 1) * animal.F)

    def get_propensity(self, animal):
        if type(self) == Ocean:
            self.propensity = 0
        elif type(self) == Mountain:
            self.propensity = 0
        else:
            self.propensity = exp(animal.lambdah * self.rel_abundance)

    def replenish(self):
        pass

    def feeding(self):
        for species in self.pop:
            self.pop[species] = sorted(self.pop[species], key=lambda x: getattr(x, 'phi'))
        for herbivore in self.pop['Herbivore']:
            herbivore.feeding(self)
        for carnivore in self.pop['Carnivore']:
            carnivore.feeding(self, self.pop['Herbivore'])

    def place_animals(self, pop_list):
        for individual_dict in pop_list:
            if individual_dict['species'] not in self.pop:
                self.pop[individual_dict['species']] = []
            new_animal = eval(individual_dict['species'])(individual_dict)
            self.pop[individual_dict['species']].append(new_animal)
            if individual_dict['species'] == 'Herbivore':
                self.tot_w_herbivores += new_animal.weight

    def procreation(self):
        N_dict = {Herbivore: self.num_specimen('Herbivore'),
                  Carnivore: self.num_specimen('Carnivore')}
        for species in self.pop.keys():
            copy = self.pop[species]
            for animal in copy:
                n = N_dict[type(animal)]
                if n >= 2:
                    if animal.fertile(n):
                        newborn = type(animal)()
                        if newborn.weight < animal.weight:
                            self.pop[species].append(newborn)
                            animal.weight -= animal.zeta * newborn.weight

    def dying(self):
        for species in self.pop:
            for animal in self.pop[species]:
                if animal.dies():
                    animal.remove(self)
                    # self.num_animals -= 1
                    # self.num_animals_per_species[type(animal).__name__] -= 1

    def migration(self, map_list):
        for species in self.pop:
            for animal in self.pop[species]:
                animal.migrate(self, map_list)

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
