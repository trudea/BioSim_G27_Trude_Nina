# -*- coding: utf-8 -*-

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"
import BioSim_G27_Trude_Nina.src.biosim.island as bs
import pytest


class TestIsland:

    def test_constructor_default(self):
        """
        A test to check if an instance of island class is created with map
        input
        """
        rossum_string = 'OOOOOOOOOOOOOOOOOOOOO\nOSSSSSJJJJMMJJJJJJJOO' \
                        '\nOSSSSSJJJJMMJJJJJJJOO\nOSSSSSJJJJMMJJJJJJJOO' \
                        '\nOOSSJJJJJJJMMJJJJJJJO\nOOSSJJJJJJJMMJJJJJJJO' \
                        '\nOOOOOOOSMMMMJJJJJJJJO\nOSSSSSJJJJMMJJJJJJJOO' \
                        '\nOSSSSSSSSSMMJJJJJJOOO\nOSSSSSDDDDDJJJJJJJOOO' \
                        '\nOSSSSSDDDDDJJJJJJJOOO\nOSSSSSDDDDDJJJJJJJOOO' \
                        '\nOSSSSSDDDDDMMJJJJJOOO\nOSSSSSDDDDDJJJJOOOOOO' \
                        '\nOOSSSDDDDDDJJOOOOOOOO\nOOSSSSDDDDDDJJOOOOOOO' \
                        '\nOSSSSSDDDDDJJJJJJJOOO\nOSSSSDDDDDDJJJJOOOOOO' \
                        '\nOOSSSSDDDDDJJJOOOOOOO\nOOOSSSSJJJJJJJOOOOOOO' \
                        '\nOOOSSSSSSOOOOOOOOOOOO\nOOOOOOOOOOOOOOOOOOOOO '
        i = bs.Island(rossum_string)
        print(i)
        assert isinstance(i, bs.Island)

    def test_map_coordinate_instance(self):
        """
        A test to check if an instance of Island given initial coordinates
        return the true biome-letter.
        """

        map = 'OOOOO\nOJJJO\nOOOOO'
        island = bs.Island(map)
        assert island.map[0][0] == 'O'

    def test_map_ocean(self):
        """
        A test that checks if ValueError is raised if there are no ocean
        tiles surrounding the island.
        """
        with pytest.raises(ValueError):
            bs.Island('SSS\nOOO')
            bs.Island('OOO\nOSS')
            bs.Island('OOO\nOSO\nOSO')

    def test_jungle_instance(self):
        """
        Checks if an instance of jungle is created by providing a jungle tile
        """
        jungle = bs.Jungle()
        assert isinstance(jungle, bs.Jungle)

    def test_desert_instance(self):
        """
        Checks if an instance of desert is created by providing a desert tile
        """
        desert = bs.Desert()
        assert isinstance(desert, bs.Desert)

    def test_ocean(self):
        """
        Checks if an instance of ocean is created by providing an ocean tile
        """
        ocean = bs.Ocean()
        assert isinstance(ocean, bs.Ocean)

    def test_mountain(self):
        """
        Checks if an instance of mountain is
        created by providing a mountain tile
        """
        mountain = bs.Mountain()
        assert isinstance(mountain, bs.Mountain)

    def test_fodder_savannah(self):
        """
        A test that tests if an instance of the Savannah class, given a
        value under f_max replenishes itself (increases the f value)
        """
        savannah = bs.Savannah()
        savannah.f = 200
        savannah.replenish()
        assert savannah.f > 200

    def test_fodder_jungle(self):
        """
        A test that checks if an instance of Jungle class, given a value
        under f_max replenishes itself to the given parameter
        f_max given to that instance of jungle.
        """
        jungle = bs.Jungle()
        jungle.f = 500
        jungle.replenish()
        assert jungle.f == jungle.param_dict['f_max']


class TestAnimal:

    def test_herbivore(self):
        """
        Checks if instance of herbivore can be created
        """
        herbivore = bs.Herbivore(None)
        assert isinstance(herbivore, bs.Herbivore)

    def test_carnivore(self):
        """
        Checks if instance of carnivore can be created
        """
        carnivore = bs.Carnivore(None)
        assert isinstance(carnivore, bs.Carnivore)

    def test_aging(self):
        """
        Checks if age of a given instance increases by call of instance.aging
        """
        herbivore = bs.Herbivore(None)
        age = herbivore.age
        herbivore.aging()
        assert herbivore.age > age

    def test_weightloss(self):
        """
        Checks if weight of an instance decreases by call of
        instance.weightloss()
        """
        herbivore = bs.Herbivore(None)
        weight = herbivore.weight
        herbivore.weightloss()
        assert herbivore.weight < weight

    def test_herbivore_feeding(self):
        """
        Checks if weight of an instance increases by call of
        instance.feeding(F)
        given initial parameter value F specific for that instance.
        """
        herbivore = bs.Herbivore(None)
        previous_weight = herbivore.weight
        feed = herbivore.param_dict['F']
        herbivore.feeding(feed)
        assert previous_weight < herbivore.weight
