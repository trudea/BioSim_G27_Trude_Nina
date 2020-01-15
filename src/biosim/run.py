# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"


#  from src.biosim.island import Island
from src.biosim.island import Island

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

    def __init__(self, desired_years=10, animal_input=None, map_input=None):
        self.desired_years = desired_years
        self.years_run = 0
        self.num_animals_results = []
        self.per_species_results = []
        if animal_input is None:
            animal_input = self.default_input
        self.island = Island(map_input)
        self.island.place_animals(animal_input)

    def one_cycle(self):
        self.island.all_cells('replenish')
        self.island.all_cells('feeding')
        self.island.all_cells('procreation')
        self.island.migration()
        self.island.all_animals('aging')
        self.island.all_animals('weightloss')
        self.island.all_cells('dying')
        self.island.update_num_animals()
        self.num_animals_results.append(self.island.num_animals)
        self.per_species_results.append(self.island.num_animals_per_species)
        print('Total: ', run.island.num_animals)
        print(run.island.num_animals_per_species)

    def run(self):
        years = 0
        run.island.update_num_animals()
        print('Total: ', run.island.num_animals)
        print(run.island.num_animals_per_species)
        while(years < self.desired_years):
            self.one_cycle()
            # print(run.num_animals_results)
            years += 1

if __name__ == "__main__":
    map = 'OOOOO\nOSSSO\nOSSSO\nOSSSO\nOOOOO'
    animals = [{'loc': (2, 2), 'pop': [
        {'species': 'Herbivore', 'age': 10, 'weight': 40.5},
        {'species': 'Herbivore', 'age': 9, 'weight': 38.3},
        {'species': 'Herbivore', 'age': 14, 'weight': 50.3},
        {'species': 'Herbivore', 'age': 5, 'weight': 36.1}]}]

    # run = Run(10, animals, map)
    run = Run()
    run.run()
