# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"


#  from src.biosim.island import Island
from BioSim_G27_Trude_Nina.src.biosim.island import Island
import matplotlib


class Run:
    default_input = [{'loc': (3, 4), 'pop': [
        {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
        {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
        {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]},
                     {'loc': (4, 4),
                      'pop': [
                          {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
                          {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
                          {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]}]

    def __init__(self, desired_years=10, input=None):
        self.desired_years = desired_years
        self.years_run = 0
        self.num_animals_results = []
        self.per_species_results = []
        if input is None:
            input = self.default_input
        self.island = Island()
        self.island.place_animals(input)

    def do_collectively(self, myfunc):
        for cell in self.island.map.values():
            for animal in cell.pop:
                myfunc(animal, cell)

    def one_cycle(self):
        self.island.replenish_all()
        self.island.feeding()
        self.island.procreation()
        self.island.migration()
        self.island.aging()
        self.island.weightloss()
        self.island.dying()
        self.island.update_num_animals()
        # kan flyttes inn i dying hvis ikke myfunc
        self.num_animals_results.append(self.island.num_animals)
        self.per_species_results.append(self.island.num_animals_per_species)

    def run(self):
        years = 0
        while(years < self.desired_years):
            self.one_cycle()
            years += 1


if __name__ == "__main__":
    run = Run()
    run.run()
    print(run.island.num_animals)
    # print(run.island.num_animals_per_species['Herbivore'])
    # print(run.island.num_animals_per_species['Carnivore'])
    print(run.num_animals_results)
    print(run.per_species_results)


