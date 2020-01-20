# -*- coding: utf-8 -*-


__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

"""
Implements a biological simulation of an island with population of herbivores
and carnivores. Landscape types consist of savannah, jungle, desert and
mountain, with surrounding ocean.
"""

import inspect
import textwrap
import matplotlib.pyplot as plt
import random
from src.biosim.landscapes import Savannah, Jungle, Desert, Mountain, Ocean
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class BioSim:
    """Define and run a biological simulation. """

    def __init__(
        self,
        island_map=None,
        ini_pop=None,
        seed=None,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",

    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing
        animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal
        densities
        :param img_base: String with beginning of file name for figures,
        including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted
        automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        self.land_dict = {'S': Savannah, 'J': Jungle, 'O': Ocean, 'M':
                          Mountain, 'D': Desert}
        self.active = {Savannah: 0, Jungle: 0, Desert: 0}
        self._year = 0

        self.num_years = 0
        self.vis_years = 0
        self.img_years = 0
        self.sim_years = 0

        self.num_animals_results = []
        self.per_species_results = []
        self.map = self.str_to_dict(island_map)
        for cell in self.map.values():
            if type(cell) in self.active:
                self.active[type(cell)] += 1
        self.map_active = {key: value for (key, value) in self.map.items() if
                           type(value) in self.active}
        self.map_inactive = {key: value for (key, value) in self.map.items() if
                           type(value) in self.active}
        self.map_copy = self.map.copy()
        self.map = self.map_active
        self.add_population(ini_pop)
        self.change = {'Born' : {'Herbivore': 0, 'Carnivore': 0}, 'Dead' : {'Herbivore': 0, 'Carnivore': 0}}


        random.seed(seed)

        if ymax_animals is None:
            # juster automatisk
            pass
        self.ymax_animals = ymax_animals
        if cmax_animals is None:
            # automatisk
            pass
        self.cmax_animals = cmax_animals
        if img_base is None:
            # automatisk
            pass
        self.img_base = img_base
        self.fmt = img_fmt

    def str_to_dict(self, txt):
        """
        Turn string into dictionary if requirements for a map string are met.

        :param txt: String of letters, each signifying the type of landscape at
         corresponding location.
        :return: dict: Dictionary with tuples of y- and x-coordinate as keys,
        and instance of landscape class as values
        """
        txt = txt.split('\n')
        if not txt[-1].isalpha():
            txt.pop()
        self.check_txt(txt)
        y = 0
        dict = {}
        for row in txt:
            x = 0
            for letter in row:
                dict[(y, x)] = self.land_dict[letter]()
                x += 1
            y += 1
        return dict
    
    def check_txt(self, txt):
        """
        Check if string meets requirements for a map string.

        :param txt: String of letters
        """

        left_column = [line[0] for line in txt]
        right_column = [line[-1] for line in txt]
        to_check = [txt[0], txt[-1], left_column, right_column]
        for list in to_check:
            for element in list:
                if element != 'O':
                    raise ValueError
        for line in txt:
            if len(line) != len(txt[0]):
                raise ValueError
        for row in txt:
            for letter in row:
                if letter not in self.land_dict:
                    raise ValueError

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        self.name = species
        # self.land_dict[].set_parameter(params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        self.land_dict[landscape].set_params(params)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files
        (default: vis_years)

        Image files will be numbered consecutively.
        """
        self.num_years = num_years
        self.vis_years = vis_years
        self.img_years = img_years
        self.sim_years = 0

        self.num_animals_results = []
        self.per_species_results = []

        while (self.sim_years < self.num_years):
            self.one_year()
            self.sim_years += 1
            # print(self.year, ' ', self.num_animals_per_species)
            for cell in self.map.values():
                for key in self.change:
                    for species in self.change[key]:
                        self.change[key][species] += cell.change[key][species]


    def one_year(self):
        """ Implement one annual cycle. """

        self.all_cells('replenish')
        self.all_cells('feeding')
        self.all_cells('procreation')
        # print('Num animals before: ', self.num_animals_per_species)
        self.migration()
        # print('Num animals after: ', self.num_animals_per_species)
        self.all_animals('aging')
        self.all_animals('weightloss')
        self.all_cells('dying')
        self.num_animals_results.append(self.num_animals)
        self.per_species_results.append(self.num_animals_per_species)
        self.year = 1
        print(self.num_animals_per_species)
        # print(self.year, ' ', self.change)

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        for loc_dict in population:
            if loc_dict['loc'] not in self.map:
                raise ValueError
            loc = self.map[loc_dict['loc']]
            loc.place_animals(loc_dict['pop'])

    @property
    def year(self):
        """Last year simulated."""
        return self._year

    @year.setter
    def year(self, n):
        self._year += n

    @property
    def num_animals(self):
        """Total number of animals on island."""
        num_animals = 0
        for cell in self.map.values():
            num_animals += len(cell.pop['Herbivore']) +\
                           len(cell.pop['Carnivore'])
        return num_animals

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        _num_animals_per_species = {'Herbivore': 0, 'Carnivore': 0}
        for cell in self.map.values():
            for species in cell.pop:
                _num_animals_per_species[species] += len(
                    cell.pop[species])
        return _num_animals_per_species

    def animal_distribution(self):
        coordinates = [cell for cell in self.map]
        dictionary = {}
        for cell in sim.map.values():
            herbivore = 0
            carnivore = 0
            for species in cell.pop:
                if species == 'Herbivore':
                    herbivore += len(cell.pop[species])
                if species == 'Carnivore':
                    carnivore += len(cell.pop[species])
            dictionary[cell] = \
                (carnivore + herbivore), herbivore, carnivore

        population = [dictionary[cell][0] for cell in dictionary]
        herbivores = [dictionary[cell][1] for cell in dictionary]
        carnivores = [dictionary[cell][2] for cell in dictionary]
        coordinates = [cell for cell in self.map]
        data = {'Cell': coordinates, 'Population': population,
                'Herbivores': herbivores, 'Carnivores': carnivores}
        return pd.DataFrame(data)

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""

    def all_cells(self, myfunc):
        """
        Execute method for every active location.

        :param myfunc: Method to be executed
        """
        for cell in self.map.values():
            getattr(cell, myfunc)()

    def all_animals(self, myfunc):
        """
        Execute method for all animals.

        :param myfunc: Method to be executed.
        """

        for cell in self.map.values():
            for species in cell.pop:
                for animal in cell.pop[species]:
                    getattr(animal, myfunc)()

    def migration(self):
        """Execute migration step of annual cycle."""
        for pos, cell in self.map.items():
            if type(cell) == Ocean or type(cell) == Mountain:
                pass
            else:
                y, x = pos
                adjecent_pos = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
                map_list = [self.map[element] for element in adjecent_pos if
                            element in self.map]
                copy = map_list
                for element in copy:
                    if type(element) == Ocean or type(element) == Mountain:
                        map_list.remove(element)
                cell.migration(map_list)


if __name__ == '__main__':
    """
    default_seed = 33
    default_txt = open('rossum.txt').read()
    default_pop = [{'loc': (3, 4), 'pop': [
        {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
        {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
        {'species': 'Carnivore', 'age': 14, 'weight': 10.3},
        {'species': 'Carnivore', 'age': 5, 'weight': 10.1}]},
                     {'loc': (4, 4),
                      'pop': [
                          {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
                          {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
                          {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]}]
    """

    # sim = BioSim(default_txt, default_pop, default_seed)
    # sim.simulate(10)
    """
    geogr = '\
               OOOOOOOOOOOOOOOOOOOOO
               OOOOOOOOSMMMMJJJJJJJO
               OSSSSSJJJJMMJJJJJJJOO
               OSSSSSSSSSMMJJJJJJOOO
               OSSSSSJJJJJJJJJJJJOOO
               OSSSSSJJJDDJJJSJJJOOO
               OSSJJJJJDDDJJJSSSSOOO
               OOSSSSJJJDDJJJSOOOOOO
               OSSSJJJJJDDJJJJJJJOOO
               OSSSSJJJJDDJJJJOOOOOO
               OOSSSSJJJJJJJJOOOOOOO
               OOOSSSSJJJJJJJOOOOOOO
               OOOOOOOOOOOOOOOOOOOOO'
    geogr = textwrap.dedent(geogr)
    """
    default_txt = open('rossum.txt').read()
    ini_herbs = [
        {
            "loc": (1, 1),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(150)
            ],
        }
    ]
    ini_carns = [
        {
            "loc": (10, 10),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(40)
            ],
        }
    ]

    sim = BioSim(default_txt, ini_herbs, 1)

    #sim.set_animal_parameters("Herbivore", {"zeta": 3.2, "xi": 1.8})
    #sim.set_animal_parameters(
    """
        "Carnivore",
        {
            "a_half": 70,
            "phi_age": 0.5,
            "omega": 0.3,
            "F": 65,
            "DeltaPhiMax": 9.0,
        },
    )
    """
    #sim.set_landscape_parameters("J", {"f_max": 700})

    #sim.simulate(num_years=2, vis_years=1, img_years=2000)


    #sim.add_population(population=ini_carns)
    #sim.simulate(num_years=2, vis_years=1, img_years=2000)






