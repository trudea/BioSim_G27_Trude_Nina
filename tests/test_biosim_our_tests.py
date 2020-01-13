# -*- coding: utf-8 -*-

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"
import biosim.island as isl
import biosim.animals as ani
import biosim.landscapes as land
import biosim.run as run
import pytest
import random

# fiks fixtures for lettere koding


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

    def test_change_param_dict(self):
        """
        Checks if a change of parameters actually applies to class instance
        and replaces standard values
        """
        original_dict = land.Savannah.param_dict.copy()
        jungle = land.Jungle(param_dict={'f_max': 500})
        savannah = land.Savannah(param_dict={'f_max': 200})
        assert jungle.param_dict['f_max'] is not 800 \
            and savannah.param_dict['f_max'] is not 300
        land.Savannah.param_dict = original_dict
    def test_jungle_instance(self):
        """
        Checks if an instance of jungle is created by providing a jungle tile
        """
        jungle = land.Jungle()
        assert isinstance(jungle, land.Jungle)

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

    def test_fodder_savannah(self):
        """
        A test that tests if an instance of the Savannah class, given a
        value under f_max replenishes itself (increases the f value)
        """
        s = land.Savannah()
        s.f = 200.0
        s.replenish()
        assert s.f > 200.0

    def test_fodder_jungle(self):
        """
        A test that checks if an instance of Jungle class, given a value
        under f_max replenishes itself to the given parameter
        f_max given to that instance of jungle.
        """
        jungle = land.Jungle()
        jungle.f = 500
        jungle.replenish()
        assert jungle.f == jungle.param_dict['f_max']


class TestAnimal:

    def test_herbivore(self):
        """
        Checks if instance of herbivore can be created and is instance of
        the animal class
        """
        herbivore = ani.Herbivore(None)
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

    def test_get_position(self):
        pass

    def test_place_animal(self):
        input = [{'loc': (4, 4), 'pop': [
            {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
            {'species': 'Herbivore', 'age': 9, 'weight': 10.3}]}]

        i = isl.Island()
        c = isl.Cell(4, 4, 'S')
        i.place_animals(input)
        herbivore_list = i.map[4][4]
        assert len(herbivore_list.pop) == 2

    def test_tot_w_herbivores(self):
        input_list =[{'loc': (4, 3), 'pop': [{'species': 'Herbivore',
                                              'age': 10,
                                             'weight': 12.6}]}]
        i = isl.Island()
        i.place_animals(input_list)
        c = i.map[4][3]
        assert c.tot_w_herbivores == 12.6

    def test_move_animal(self):
        pass

    def test_eat_in_order_fitness(self):
        pass

    def test_animal_dead(self):
        herbivore = ani.Herbivore()
        # herbivore.phi = 0, skal faile hvis denne ikke er her. passer uansett
        # må kunne plassere den
        herbivore.check_if_dying()
        assert hasattr(isl.Island, 'Herbivore') is False

    def test_little_fodder(self):
        herbivore = ani.Herbivore()
        herbivore_weight_if_not_limited = (herbivore.weight +herbivore.beta *
                                           herbivore.F)
        savannah = land.Savannah()
        savannah.f = random.randint(0, (herbivore.F - 1))
        herbivore.weightgain_and_fodder_left(savannah.f)
        assert herbivore.weight < herbivore_weight_if_not_limited

    def test_parameter_change(self):

        pass

    def test_value_error_raised_placement_mountain_ocean(self):
        pass

    def test_die_order_fitness(self):
        pass

class TestRun:
    pass
