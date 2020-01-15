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
        self.species_to_class = dict(inspect.getmembers(animals, inspect.isclass))
        del self.species_to_class['Animal']
        self.pop = {'Herbivore': [], 'Carnivore': []}
        self.tot_w_herbivores = \
            sum([herbivore.weight for herbivore in self.pop['Herbivore']])
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

    def update_num_animals(self):
        for species in self.pop:
            for animal in self.pop[species]:
                self.num_animals_per_species[type(animal).__name__] += 1
                self.num_animals += 1


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

    def replenish(self):
        pass

    def feeding(self):
        for species in self.pop:
            species = sorted(self.pop[species],
                             key=lambda x: getattr(x, 'phi'))
        for herbivore in self.pop['Herbivore']:
            self.f = herbivore.weightgain_and_fodder_left(self.f)
        for carnivore in self.pop['Carnivore']:
            eaten = 0
            copy = self.pop['Herbivore']
            for prey in copy:  # use filtering
                if eaten < carnivore.F:
                    if carnivore.check_if_kills(prey):
                        carnivore.gaining_weight(prey.weight)
                        carnivore.evaluate_fitness()
                        self.remove_animal(prey)
                        #self.num_animals -= 1
                        #self.num_animals_per_species['Herbivore'] -= 1
                        self.update_num_animals()

    def place_animals(self, pop_list):
        for individual_dict in pop_list:
            if individual_dict['species'] not in self.pop:
                self.pop[individual_dict['species']] = []
            new_animal = eval(individual_dict['species'])(individual_dict)
            self.pop[individual_dict['species']].append(new_animal)
            # self.num_animals += 1
            # self.num_animals_per_species[type(new_animal).__name__] += 1
            if individual_dict['species'] == 'Herbivore':
                self.tot_w_herbivores += new_animal.weight
            self.update_num_animals() # kanskje mer effektivt å endre variablen

    def procreation(self):
        N_dict = {Herbivore: self.num_specimen(Herbivore),
                  Carnivore: self.num_specimen(Carnivore)}
        newborns = 0
        for species in self.pop.keys():
            copy = self.pop[species]
            for animal in copy:
                n = N_dict[type(animal)]
                if n >= 2:
                    if animal.check_if_procreates(n):
                        newborn = type(animal)()
                        if newborn.weight < animal.weight:
                            self.pop.append(newborn)
                            animal.weight -= animal.zeta * newborn.weight
                            #self.num_animals += 1
                            #self.num_animals_per_species[type(animal)] += 1
        self.update_num_animals()



    def dying(self):
        for species in self.pop:
            for animal in self.pop[species]:
                if animal.dies():
                    self.remove_animal(animal)
                    self.num_animals -= 1
                    self.num_animals_per_species[type(animal).__name__] -= 1
        self.update_num_animals()

    def remove_animal(self, animal):
        self.pop[type(animal).__name__].remove(animal)
        self.update_num_animals()



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
