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
        self.species_to_class = dict(inspect.getmembers(animals, inspect.isclass))
        del self.species_to_class['Animal']
        self.pop = {'Herbivore': [], 'Carnivore': []}
        self.tot_w_herbivores = \
            sum([herbivore.weight for herbivore in self.pop['Herbivore']])
        self.rel_abundance = None
        self.propensity = None
        self.likelihood = None
        self.corpses = 0
        self.newborns = 0

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

        elif type(animal) == Carnivore:
            fodder = self.tot_w_herbivores

        n = self.num_specimen(type(animal).__name__)
        #print(fodder / ((n + 1) * animal.F))
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
            carnivore.feeding(self)

    def place_animals(self, pop_list):
        for individual_dict in pop_list:
            if individual_dict['species'] not in self.pop:
                self.pop[individual_dict['species']] = []
            new_animal = eval(individual_dict['species'])(individual_dict)
            self.pop[individual_dict['species']].append(new_animal)
            if individual_dict['species'] == 'Herbivore':
                self.tot_w_herbivores += new_animal.weight

    def procreation(self):
        for species, pop_list in self.pop.items():
            copy = pop_list
            for animal in copy:
                n = self.num_specimen(species)
                if n >= 2:
                    if animal.fertile(n):
                        newborn = type(animal)()
                        if animal.weight >= animal.zeta * (newborn.weight + animal.sigma_birth):
                            q = len(pop_list)
                            self.pop[species].append(newborn)
                            if len(pop_list) <= q:
                                print('Pop list not updated')
                            animal.weight -= animal.zeta * newborn.weight
                            if animal.weight <0:
                                print('animal weight too small after birth')

    def dying(self):
        for species in self.pop:
            self.pop[species] = [animal for animal in self.pop[species] if not animal.dies()]

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
