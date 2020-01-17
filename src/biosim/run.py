# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"


#  from src.biosim.island import Island
from src.biosim.island import Island
import random
from src.biosim.animals import Carnivore, Herbivore

#import matplotlib.pyplot as plt


class Run:
    default_input = [{'loc': (3, 4), 'pop': [
        {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
        {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
        {'species': 'Carnivore', 'age': 14, 'weight': 10.3},
        {'species': 'Carnivore', 'age': 5, 'weight': 10.1}]},
                     {'loc': (4, 4),
                      'pop': [
                          {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
                          {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
                          {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]}]
    herbivore_input = [{'loc': (3, 4), 'pop': [
        {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
        {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
        {'species': 'Herbivore', 'age': 14, 'weight': 10.3},
        {'species': 'Herbivore', 'age': 5, 'weight': 10.1}]},
                     {'loc': (4, 4),
                      'pop': [
                          {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
                          {'species': 'Herbivore', 'age': 3, 'weight': 7.3},
                          {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]}]

    def __init__(self, ini_pop = None, island_map = None, seed = None):

        self.desired_years = 10
        self.num_animals_results = []
        self.per_species_results = []
        if ini_pop is None:
            ini_pop = self.herbivore_input
        self.island = Island(island_map)
        self.island.place_animals(ini_pop)

    def one_cycle(self):
        self.island.all_cells('replenish')
        self.island.all_cells('feeding')
        carnilist = list_carnivores()
        carniw = [carni.weight for carni in carnilist]
        self.island.all_cells('procreation')
        carnilist = list_carnivores()
        weights = [carni.weight for carni in carnilist]
        for i in range(len(weights)):
            #print(weights[i] - carniw[i])
            pass
        self.island.migration()
        self.island.all_animals('aging')
        self.island.all_animals('weightloss')
        self.island.all_cells('dying')
        self.island.update_num_animals()
        self.num_animals_results.append(self.island.num_animals)
        self.per_species_results.append(self.island.num_animals_per_species)

    def run(self):
        self.years = 0
        self.desired_years = 50
        while(self.years < self.desired_years):
            print(run.island.num_animals_per_species)
            self.one_cycle()
            self.years += 1
            # print(self.years)



if __name__ == "__main__":
    map = 'OOOOO\nOJJJO\nOJJJO\nOJJJO\nOJJJO\nOOOO'
    animals = [{'loc': (1, 1), 'pop': [
        {'species': 'Herbivore', 'age': 10, 'weight': 40.5},
        {'species': 'Herbivore', 'age': 9, 'weight': 38.3},
        {'species': 'Herbivore', 'age': 14, 'weight': 50.3},
        {'species': 'Herbivore', 'age': 5, 'weight': 36.1}]},
               {'loc': (2, 2), 'pop': [
                   {'species': 'Herbivore', 'age': 10, 'weight': 40.5},
                   {'species': 'Herbivore', 'age': 9, 'weight': 38.3},
                   {'species': 'Herbivore', 'age': 14, 'weight': 50.3},
                   {'species': 'Herbivore', 'age': 5, 'weight': 36.1}]}

               ]







    map = 'OOOOOOO\nOJJJJJO\nOJJJJJO\nOJJJJJO\nOJJJJJO\nOJJJJJO\nOJJJJJO\nOOOOOOO'

    # island = Island()
    run = Run()

    cell = run.island.map[(1, 1)]
    for i in range(5):
        cell.pop['Herbivore'].append(Herbivore())
        cell.pop['Herbivore'].append(Herbivore())
        cell.pop['Herbivore'].append(Herbivore())
    cell = run.island.map[(2, 2)]
    for i in range(5):
        cell.pop['Herbivore'].append(Herbivore())
        cell.pop['Herbivore'].append(Herbivore())
        cell.pop['Herbivore'].append(Herbivore())
    cell = run.island.map[(1, 2)]
    for i in range(5):
        cell.pop['Herbivore'].append(Herbivore())
        cell.pop['Herbivore'].append(Herbivore())
        cell.pop['Herbivore'].append(Herbivore())
    cell = run.island.map[(2, 1)]
    for i in range(5):
        cell.pop['Herbivore'].append(Herbivore())
        cell.pop['Herbivore'].append(Herbivore())
        cell.pop['Herbivore'].append(Herbivore())


    def list_herbivores():
        all_herbivores = []
        for cell in run.island.map.values():
            if len(cell.pop['Herbivore']) > 0:
                for element in cell.pop['Herbivore']:
                    all_herbivores.append(element)
        return all_herbivores


    def list_carnivores():
        all_carnivores = []
        for cell in run.island.map.values():
            if len(cell.pop['Carnivore']) > 0:
                for element in cell.pop['Carnivore']:
                    all_carnivores.append(element)
        return all_carnivores

    run.run()

    for i in range(100):
        run.island.map[(1, 1)].pop['Carnivore'].append(Carnivore())
        run.island.map[(2, 2)].pop['Carnivore'].append(Carnivore())
        run.island.map[(3, 3)].pop['Carnivore'].append(Carnivore())
        run.island.map[(1, 1)].pop['Carnivore'].append(Carnivore())
        run.island.map[(2, 2)].pop['Carnivore'].append(Carnivore())
        run.island.map[(3, 3)].pop['Carnivore'].append(Carnivore())
        run.island.map[(1, 1)].pop['Carnivore'].append(Carnivore())
        run.island.map[(2, 2)].pop['Carnivore'].append(Carnivore())
        run.island.map[(3, 3)].pop['Carnivore'].append(Carnivore())
        run.island.map[(1, 1)].pop['Carnivore'].append(Carnivore())
        run.island.map[(2, 2)].pop['Carnivore'].append(Carnivore())
        run.island.map[(3, 3)].pop['Carnivore'].append(Carnivore())
    run.island.update_num_animals()
    # print(run.island.num_animals_per_species)

    run.run()
