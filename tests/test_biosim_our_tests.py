# -*- coding: utf-8 -*-

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"
import BioSim_G27_Trude_Nina.src.biosim.island as isl
import BioSim_G27_Trude_Nina.src.biosim.animals as ani
import BioSim_G27_Trude_Nina.src.biosim.landscapes as land
import BioSim_G27_Trude_Nina.src.biosim.run as run
import pytest


class TestIsland:

    def test_constructor_default(self):
        """
        A test to check if an instance of island class is created
        without input
        """
        i = isl.Island()
        assert isinstance(i, isl.Island)

    def test_constructor_input(self):
        """
        A test to check if an instance of island class is created
        with input
        """
        map = 'OOOOO\nOJJJO\nOOOOO'
        i = isl.Island(map)
        assert isinstance(i, isl.Island)

    def test_map_coordinate_instance(self):
        """
        A test to check if an instance of Island given initial coordinates
        return the true biome-letter.
        """
        map = 'OOOOO\nOJJJO\nOOOOO'
        island = isl.Island(map)
        assert type(island.map[0][0].landscape).__name__ == 'Ocean'

    def test_map_ocean(self):
        """
        A test that checks if ValueError is raised if there are no ocean
        tiles surrounding the island.
        """
        with pytest.raises(ValueError):
            isl.Island('SSS\nOOO')
            isl.Island('OOO\nOSS')
            isl.Island('OOO\nOSO\nOSO')


class TestLandscapes:

    def test_jungle_instance(self):
        """
        Checks if an instance of jungle is created by providing a jungle tile
        """
        jungle = isl.Jungle()
        assert isinstance(jungle, isl.Jungle)

    def test_desert_instance(self):
        """
        Checks if an instance of desert is created by providing a desert tile
        """
        desert = isl.Desert()
        assert isinstance(desert, isl.Desert)

    def test_ocean(self):
        """
        Checks if an instance of ocean is created by providing an ocean tile
        """
        ocean = isl.Ocean()
        assert isinstance(ocean, isl.Ocean)

    def test_mountain(self):
        """
        Checks if an instance of mountain is
        created by providing a mountain tile
        """
        mountain = isl.Mountain()
        assert isinstance(mountain, isl.Mountain)

    def test_fodder_savannah(self):
        """
        A test that tests if an instance of the Savannah class, given a
        value under f_max replenishes itself (increases the f value)
        """
        savannah = isl.Savannah()
        savannah.f = 200
        savannah.replenish()
        assert savannah.f > 200

    def test_fodder_jungle(self):
        """
        A test that checks if an instance of Jungle class, given a value
        under f_max replenishes itself to the given parameter
        f_max given to that instance of jungle.
        """
        jungle = isl.Jungle()
        jungle.f = 500
        jungle.replenish()
        assert jungle.f == jungle.param_dict['f_max']


class TestAnimal:

    def test_herbivore(self):
        """
        Checks if instance of herbivore can be created and is instance of
        the animal class
        """
        herbivore = isl.Herbivore(None)
        assert isinstance(herbivore, ani.Animal)

    def test_carnivore(self):
        """
        Checks if instance of carnivore can be created and is instance
        of the animal class
        """
        carnivore = ani.Carnivore(None)
        assert isinstance(carnivore, ani.Animal)

    def test_aging(self):
        """
        Checks if age of a given instance increases by call of instance.aging
        """
        herbivore = ani.Herbivore(None)
        age = herbivore.age
        herbivore.aging()
        assert herbivore.age > age

    def test_weightloss(self):
        """
        Checks if weight of an instance decreases by call of
        instance.weightloss()
        """
        herbivore = ani.Herbivore(None)
        weight = herbivore.weight
        herbivore.losing_weight()
        assert herbivore.weight < weight

    def test_herbivore_feeding(self):
        """
        Checks if weight of an instance increases by call of
        instance.feeding(F)
        given initial parameter value F specific for that instance.
        """
        herbivore = ani.Herbivore(None)
        previous_weight = herbivore.weight
        feed = herbivore.param_dict['F']
        herbivore.gaining_weight(feed)
        assert previous_weight < herbivore.weight
