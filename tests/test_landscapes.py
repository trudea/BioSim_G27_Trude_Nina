# -*- coding: utf-8 -*-

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"
import src.biosim.animals as ani
import src.biosim.landscapes as land
import src.biosim.simulation as sim
import pytest
import random

@pytest.fixture
def input_list():
    return [
        {'loc': (1, 1),
         'pop': [
         {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
         {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
         {'species': 'Carnivore', 'age': 14, 'weight': 10.3},
         {'species': 'Carnivore', 'age': 5, 'weight': 10.1}]},
        {'loc': (1, 2),
         'pop': [
          {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
          {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
          {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]},
        {'loc': (1, 2),
         'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 12.6}]}]


@pytest.fixture
def example_savannah():
    params = land.Savannah.params.copy()
    yield land.Savannah()
    land.Savannah.params = params


@pytest.fixture
def example_jungle():
    params = land.Jungle.params.copy()
    yield land.Jungle()
    land.Jungle.params = params


@pytest.fixture
def example_map():
    return """OOOO\nOJJO\nOOOO"""


class TestLandscapes:

    def test_change_param_dict(self):
        """
        Checks if a change of parameters actually applies to class instance
        and replaces standard values
        """
        original_dict = land.Savannah.params.copy()
        jungle = land.Jungle(param_dict={'f_max': 500})
        savannah = land.Savannah({'f_max': 200})
        assert jungle.params['f_max'] is not 800 \
            and savannah.params['f_max'] is not 300
        land.Savannah.params = original_dict

    def test_jungle_instance(self, example_jungle):
        """
        Checks if an instance of jungle is created by providing a jungle tile
        """
        assert isinstance(example_jungle, land.Jungle)

    def test_desert_instance(self):
        """
        Checks if an instance of desert is created by providing a desert tile
        """
        desert = land.Desert()
        assert isinstance(desert, land.Desert)

    def test_ocean(self):
        """
        Checks if an instance of ocean is created by providing an ocean tile
        """
        ocean = land.Ocean()
        assert isinstance(ocean, land.Ocean)

    def test_mountain(self):
        """
        Checks if an instance of mountain is
        created by providing a mountain tile
        """
        mountain = land.Mountain()
        assert isinstance(mountain, land.Mountain)

    def test_fodder_savannah(self, example_savannah):
        """
        A test that tests if an instance of the Savannah class, given a
        value under f_max replenishes itself (increases the f value)
        """
        example_savannah.f = 200.0
        example_savannah.replenish()
        assert example_savannah.f > 200.0

    def test_fodder_jungle(self, example_jungle):
        """
        A test that checks if an instance of Jungle class, given a value
        under f_max replenishes itself to the given parameter
        f_max given to that instance of jungle.
        """
        example_jungle.f = 500
        example_jungle.replenish()
        assert example_jungle.f == example_jungle.params['f_max']

    def test_num_animals(self, input_list, example_map):
        island = sim.BioSim(example_map, input_list, None)
        island.add_population(input_list)
        assert island.num_animals == 8

    def test_num_animals_per_species(self, input_list, example_map):
        island = sim.BioSim(example_map, input_list, None)
        assert island.num_animals_per_species['Herbivore'] == 4

    def test_relative_abundance(self, example_jungle):
        assert example_jungle._rel_abundance == 700