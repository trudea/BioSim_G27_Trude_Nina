# -*- coding: utf-8 -*-

from biosim.island import Island

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

import inspect
import random
from src.biosim.animals import Herbivore, Carnivore
from src.biosim.landscapes import Savannah, Jungle, Desert, Mountain, Ocean
import pandas as pd


class BioSim:
    def __init__(
        self,
        island_map,
        ini_pop,
        seed,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",

    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        self.land_dict = {'S': Savannah, 'J': Jungle, 'O': Ocean, 'M': Mountain, 'D': Desert}
        self.map = island_map
        self.years = 0
        self.default_pop = [{'loc': (3, 4), 'pop': [
            {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
            {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
            {'species': 'Carnivore', 'age': 14, 'weight': 10.3},
            {'species': 'Carnivore', 'age': 5, 'weight': 10.1}]},
                            {'loc': (4, 4),
                             'pop': [
                                 {'species': 'Herbivore', 'age': 10,
                                  'weight': 12.5},
                                 {'species': 'Carnivore', 'age': 3,
                                  'weight': 7.3},
                                 {'species': 'Carnivore', 'age': 5,
                                  'weight': 8.1}]}]
        if ini_pop is None:
            self.ini_pop = self.default_pop

        self.map = self.str_to_dict(island_map)

        self.place_animals(self.default_pop)

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
        # lage img_no?
    
    def str_to_dict(self, txt):
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

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        landscape = landscape.split
        list_landscape = []
        for line in landscape:
            list_landscape.append([line])

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """
        self.num_years = num_years
        self.vis_years = vis_years
        self.img_years = img_years

        self.num_animals_results = []
        self.per_species_results = []

        while (self.years < self.num_years):
            print(self.num_animals_per_species)
            self.all_cells('replenish')
            self.all_cells('feeding')
            self.all_cells('procreation')
            self.migration()
            self.all_animals('aging')
            self.all_animals('weightloss')
            self.all_cells('dying')
            # self.update_num_animals()
            self.num_animals_results.append(self.num_animals)
            self.per_species_results.append(self.num_animals_per_species)
            self.years += 1

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        for individual_dict in population:
            if individual_dict['species'] not in self.pop:
                self.pop[individual_dict['species']] = []
            new_animal = eval(individual_dict['species'])(individual_dict)
            self.pop[individual_dict['species']].append(new_animal)
            if individual_dict['species'] == 'Herbivore':
                self.tot_w_herbivores += new_animal.weight
        return


    """ property fungerer ved at den gjør metoder om til objekter
    se https://www.journaldev.com/14893/python-property-decorator for mer
    basically: en metode num_animals() kan kalles kun ved num_animals
    """

    @property
    def year(self):
        """Last year simulated."""
        return self.year

    @property
    def num_animals(self):
        """Total number of animals on island."""

        num_animals = 0
        num_animals_per_species: {'Herbivore': 0, 'Carnivore': 0}
        for cell in self.map.values():
            num_animals += len(cell.pop['Herbivore']) + len(cell.pop[Carnivore])
        return num_animals

        return self.num_animals

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""

        num_animals_per_species: {'Herbivore': 0, 'Carnivore': 0}
        for cell in self.map.values():
            for species in self.num_animals_per_species:
                self.num_animals_per_species[species] += len(cell.pop[species])
        return num_animals_per_species
        return self.num_animals_per_species

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species
         for each cell on island."""
        print("Creating table")
        data = {'Population': self.num_animals, 'Herbivores':
                self.num_animals_per_species['Herbivore'],
                'Carnivore': self.num_animals_per_species['Carnivore']}
        return pd.DataFrame(data)


    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""

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

    def all_cells(self, myfunc):
        for cell in self.map.values():
            getattr(cell, myfunc)()

    def all_animals(self, myfunc):
        for cell in self.map.values():
            for species in cell.pop:
                for animal in cell.pop[species]:
                    getattr(animal, myfunc)()

    def place_animals(self, input_list):
        for placement_dict in input_list:
            pos = placement_dict['loc'] # bør flytte resten til celle?
            self.map[pos].place_animals(placement_dict['pop'])

    def migration(self): # husk filtering
        for pos, cell in self.map.items():
            if type(cell) == Ocean or type(cell) == Mountain:
                pass
            else:
                y, x = pos
                adjecent_pos = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)] # må ta høyde for edges
                map_list = [self.map[element] for element in adjecent_pos]
                for element in map_list:
                    if type(element) == Ocean or type(element) == Mountain:
                        map_list.remove(element)
                cell.migration(map_list)


if __name__ == '__main__':
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

    sim = BioSim(default_txt, default_pop, default_seed)
    sim.add_population(default_pop)
    sim.simulate(1)
