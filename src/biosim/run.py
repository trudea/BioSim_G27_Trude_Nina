# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"


from .landscapes import Savannah, Jungle, Ocean, Mountain, Desert
from .animals import Herbivore, Carnivore, bubble_sort_animals
from .island import Island, Cell


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
        if input is None:
            input = self.default_input
        self.island = Island()
        self.island.place_animals(input)

    def collective_replenishing(self):
        for row in self.island.map:
            for cell in row:
                if type(cell) == Savannah or type(cell) == Jungle:
                    cell.landscape.replenish()

    def collective_feeding(self):
        active = [Savannah, Jungle, Desert]
        for row in self.island.map:
            for cell in row:
                if type(cell) in active and len(cell.pop) > 0:
                    cell.pop = self.bubble_sort_animals(cell.pop)
                    for animal in cell.pop:
                        if type(animal) == Herbivore:
                            cell.landscape.f = \
                                animal.weightgain_and_fodder_left()

                    for animal in cell.pop:
                        if type(animal) == Carnivore:
                            eaten = 0
                            for other_animal in cell.pop:
                                # unngår while for at
                                # ikke skal gjentas selv om carn ikke mett
                                if eaten < animal.F and type(
                                        other_animal) == Herbivore:
                                    if animal.check_if_kills(other_animal):
                                        animal.gaining_weight(
                                            other_animal.weight)
                                        animal.evaluate_fitness()
                                        self.remove_animal(cell, other_animal)

    def collective_procreation(self):
        species_dict = [Herbivore, Carnivore]
        for row in self.island.map:
            for cell in row:
                # N må være lowercase, PEP-8 violation
                N_dict = {Herbivore:
                          cell.num_specimen(Herbivore),
                          Carnivore: cell.num_specimen(Carnivore)}
                for animal in cell.pop:
                    # N lowercase, PEP-8 coding style violation
                    N = N_dict[type(animal)]
                    if N >= 2:
                        if animal.check_if_procreates(N):
                            newborn = cell.pop.append(type(animal)())
                            if newborn.weight < animal.weight:
                                cell.pop.append(newborn)
                                animal.weight -= animal.zeta * newborn.weight

    """
    def collective_migration(self):
        for row in self.island.map:
            for cell in row:
                for animal in cell.pop:
                    if animal.check_if_animal_moves:
                        new_cell = self.island.choose_new_cell(cell, animal)
                        self.island.move_animal(cell, new_cell, animal)


    def collective_aging(self):
        for row in self.island.map:
            for cell in row:
                for animal in cell.pop:
                    animal.aging()

    def collective_weightloss(self):
        for row in self.island.map:
            for cell in row:
                for animal in cell.pop:
                    animal.losing_weight()

    def collective_dying(self):
        for row in self.island.map:
            for cell in row:
                for animal in cell.pop:
                    if animal.check_if_dying():
                        self.island.remove_animal(cell, animal)
                        
    """

    def migration(self, animal, cell):
        if animal.check_if_animal_moves:
            new_cell = self.island.choose_new_cell(cell, animal)
            self.island.move_animal(cell, new_cell, animal)

    def aging(self, animal, cell):
        animal.aging()

    def weightloss(self, animal, cell):
        animal.losing_weight()

    def dying(self, animal, cell):
        if animal.check_if_dying():
            self.island.remove_animal(cell, animal)

    def do_collectively(self, myfunc):
        for row in self.island.map:
            for cell in row:
                for animal in cell.pop:
                    myfunc(animal, cell)

    def one_cycle(self):
        self.collective_replenishing()
        self.collective_feeding()
        self.collective_procreation()
        # self.collective_migration()
        self.do_collectively(self.migration)
        # self.collective_aging()
        self.do_collectively(self.aging)
        # self.collective_weightloss()
        self.do_collectively(self.weightloss)
        # self.collective_dying()
        self.do_collectively(self.dying)

    def run(self):
        years = 0
        while(years < self.desired_years):
            self.one_cycle()
            years += 1


if __name__ == "__main__":
    run = Run()
    run.run()






















