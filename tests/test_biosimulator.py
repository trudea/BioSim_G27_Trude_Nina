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


class TestBioSim:

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
