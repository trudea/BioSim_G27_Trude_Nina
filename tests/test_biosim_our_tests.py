# -*- coding: utf-8 -*-

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"
import src.biosim.animals as ani
import src.biosim.landscapes as land
import src.biosim.simulation as sim
import pytest
import random

# fiks fixtures for lettere koding


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
def example_herbivore():
    default_params = ani.Herbivore.params.copy()
    yield ani.Herbivore()
    ani.Herbivore.params = default_params


@pytest.fixture
def example_carnivore():
    default_params = ani.Carnivore.params.copy()
    yield ani.Carnivore()
    ani.Herbivore.params = default_params


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


class TestIsland:

    def test_constructor_default(self):
        """
        A test to check if an instance of island class is created
        without input
        """
        s = sim.BioSim(None, None, None)
        assert isinstance(s, sim.BioSim)

    def test_constructor_input(self, example_map, input_list):
        """
        A test to check if an instance of island class is created
        with input
        """
        i = sim.BioSim(example_map, input_list, None)
        assert isinstance(i, sim.BioSim)

    def test_map_coordinate_instance(self, example_map, input_list):
        """
        A test to check if an instance of Island given initial coordinates
        return the true biome-letter.
        """
        island = sim.BioSim(example_map, input_list, None)
        coordinate = island.map[(0, 0)]
        assert type(coordinate).__name__ is 'Ocean'

    def test_map_ocean(self):
        """
        A test that checks if ValueError is raised if there are no ocean
        tiles surrounding the island.
        """
        with pytest.raises(ValueError):
            sim.BioSim('SSS\nOOO', None, None) and \
                sim.BioSim('OOO\nOSS', None, None) and \
                sim.BioSim('OOO\nOSO\nOSO', None, None)

    def test_invalid_landscape(self):
        with pytest.raises(ValueError):
            sim.BioSim("OOO\nORO\nOOO", None, None)

    def test_different_length(self):
        with pytest.raises(ValueError):
            sim.BioSim("OOOO\nOMO\nOOO", None, None)


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




class TestSimulation:

    def test_one_year(self):
        t = sim.BioSim(None, None, None).one_year()
        assert sim.BioSim.year == 1

    def test_kill_check(mocker):
        mocker.patch('random.random', return_value=0.001)
        h = ani.Herbivore({'phi': 0.2})
        c1 = ani.Carnivore({'phi': 0.9})
        c2 = ani.Carnivore({'phi': 0.2})
        c3 = ani.Carnivore({'phi': 0.1})
        assert c1.check_if_kills(h)
        assert not c2.check_if_kills(h)
        assert not c3.check_if_kills(h)

    def test_animal_distribution(self):
        pass
