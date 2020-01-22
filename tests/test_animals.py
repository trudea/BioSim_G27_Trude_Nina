# -*- coding: utf-8 -*-

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

import pytest
import random
import src.biosim.animals as ani
import src.biosim.landscapes as land
import src.biosim.simulation as sim


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

class TestAnimal:

    def test_herbivore(self, example_herbivore):
        """
        Checks if instance of herbivore can be created and is instance of
        the animal class
        """
        assert isinstance(example_herbivore, ani.Animal)

    def test_carnivore(self, example_carnivore):
        """
        Checks if instance of carnivore can be created and is instance
        of the animal class
        """
        assert isinstance(example_carnivore, ani.Animal)

    def test_aging(self, example_herbivore):
        """
        Checks if age of a given instance increases by call of instance.aging
        """
        old_age = example_herbivore.age
        example_herbivore.aging()
        assert example_herbivore.age > old_age

    def test_weightloss(self, example_herbivore):
        """
        Checks if weight of an instance decreases by call of
        instance.weightloss()
        """
        old_weight = example_herbivore.weight
        example_herbivore.weightloss()
        assert example_herbivore.weight < old_weight

    def test_herbivore_feeding(self, example_herbivore, example_savannah):
        """
        Checks if weight of an instance increases by call of
        instance.feeding(F)
        given initial parameter value F specific for that instance.
        """
        previous_weight = example_herbivore.weight
        example_herbivore.feeding(example_savannah)
        assert previous_weight < example_herbivore.weight

    def test_place_animal(self, input_list, example_map):
        i = sim.BioSim(example_map, input_list, None)
        herbivore_list = i.map[(1, 1)]
        assert len(herbivore_list.population['Herbivore']) == 2

    def test_tot_w_herbivores(self, input_list, example_map):
        i = sim.BioSim(example_map, input_list, None)
        c = i.map[(1, 1)]
        assert c.tot_w_herbivores == 22.8

    def test_move_check(self):
        """
        A test that ensures that the boolean check_if_animal_moves behaves
        accordingly
        """
        random.seed(1)
        harold = ani.Herbivore({'phi': 0})  # asserts probability of
        # moving is high
        assert harold.movable()

    def test_migration(self, example_carnivore):
        cell1, cell2 = land.Savannah(), land.Savannah()
        cell1.population["Carnivore"].append(example_carnivore)
        example_carnivore.move(cell1, cell2)
        assert len(cell2.population["Carnivore"]) == 1

    def test_eat_in_order_fitness(self, example_savannah):
        herbert, herman = ani.Herbivore(), ani.Herbivore()
        herbert.weight, herbert.phi, herman.weight, herman.phi = 10, 10, 1, 0.5
        example_savannah.f = (herbert.params['F'] - 1)
        example_savannah.pop['Herbivore'].append(herbert)
        example_savannah.pop['Herbivore'].append(herman)
        example_savannah.feeding()
        assert herbert.weight > herman.weight

    def test_check_kills(self, example_herbivore, example_carnivore):
        random.seed(999)
        herman = ani.Herbivore({'phi': 0})
        # asserts that the probability of killing is high
        carnie = ani.Carnivore({'phi': 1})
        assert carnie.check_if_kills(herman)

    def test_animal_dead(self):
        herbert = ani.Herbivore({'phi': 0})
        assert herbert.dies()

    def test_animal_dead_is_removed(self):
        herman = ani.Herbivore({'phi': 0})
        example_savannah.pop['Herbivore'].append(herman)
        example_savannah.dying()
        assert herman not in example_savannah.pop['Herbivore']

    def test_little_fodder(self, example_herbivore):
        herbivore = example_herbivore
        herbivore_weight_if_not_limited = (herbivore.weight + herbivore.beta *
                                           herbivore.F)
        savannah = land.Savannah()
        savannah.f = random.randint(0, (herbivore.F - 1))
        savannah.feeding()
        assert herbivore.weight < herbivore_weight_if_not_limited

    def test_check_procreation(self, example_carnivore):
        random.seed(999)
        example_carnivore.weight = 45
        assert example_carnivore.fertile(90)

    def test_new_individual(self, example_herbivore, example_savannah):
        random.seed(999)
        example_herbivore.weight = 45
        for i in range(5):
            example_savannah.pop['Herbivore'].append(example_herbivore)
        old_pop = len(example_savannah.pop['Herbivore'])
        example_savannah.procreation()
        new_pop = len(example_savannah.pop['Herbivore'])
        assert new_pop > old_pop

    def test_parameter_change(self, example_carnivore):
        old_parameter = example_carnivore.params["w_birth"]
        example_carnivore.params["w_birth"] = 10
        assert example_carnivore.params["w_birth"] is not old_parameter

    def test_value_error_raised_placement_mountain_ocean(self):
        test_map = 'OOOO\nOMDO\nOOO'
        input = [{'loc': (1, 1), 'pop': [{'species': 'Herbivore', 'age': 10,
                                          'weight': 12.5}]}]
        with pytest.raises(ValueError):
            sim.BioSim(test_map, input, None)

    def test_kill_order_fitness(self):
        cell = land.Jungle()
        herb, herman = ani.Herbivore({'phi': 0.5}), ani.Herbivore({'phi': 1})
        killer = ani.Carnivore({'phi': 1})
        cell.pop.add(herb, herman, killer)
        land.LandscapeCell.feeding(cell)
        assert cell.pop == 2