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
        {'loc': (3, 4),
         'pop': [
         {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
         {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
         {'species': 'Carnivore', 'age': 14, 'weight': 10.3},
         {'species': 'Carnivore', 'age': 5, 'weight': 10.1}]},
        {'loc': (4, 4),
         'pop': [
          {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
          {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
          {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]},
        {'loc': (2, 2),
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

    def test_constructor_input(self, example_map):
        """
        A test to check if an instance of island class is created
        with input
        """
        i = sim.BioSim(example_map, None, None)
        assert isinstance(i, sim.BioSim)

    def test_map_coordinate_instance(self, example_map):
        """
        A test to check if an instance of Island given initial coordinates
        return the true biome-letter.
        """
        island = sim.BioSim(example_map, None, None)
        coordinate = island.map([0, 0])
        assert type(coordinate).__name__ is 'Ocean'

    def test_map_ocean(self):
        """
        A test that checks if ValueError is raised if there are no ocean
        tiles surrounding the island.
        """
        with pytest.raises(ValueError):
            isl.Island('SSS\nOOO') and \
                isl.Island('OOO\nOSS') and \
                isl.Island('OOO\nOSO\nOSO')

    def test_invalid_landscape(self):
        with pytest.raises(ValueError):
            isl.Island("OOO\nORO\nOOO")


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
        assert example_jungle.f == example_jungle.param_dict['f_max']

    def test_num_animals_per_species(self, input_list, example_map):
        island = isl.Island()
        island.place_animals(input_list)
        assert island.num_animals_per_species['Herbivore'] == 4

    def test_num_specimen(self, input_list):
        isl.Island().place_animals(input_list)
        isl.Island().update_num_animals()
        assert isl.Island().map[(2, 2)].num_specimen("Herbivore") == 1

    def test_relative_abundance(self, input_list, example_carnivore):
        isl.Island().place_animals(input_list)
        isl.Island().update_num_animals()
        assert isl.Island().map[(3, 4)].get_rel_abundance(example_carnivore) \
        == 22.8


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

    def test_place_animal(self, input_list):
        i = isl.Island()
        i.place_animals(input_list)
        herbivore_list = i.map[4, 4]
        assert len(herbivore_list.pop) == 2

    def test_tot_w_herbivores(self, input_list):
        i = isl.Island()
        i.place_animals(input_list)
        c = i.map[3, 4]
        assert c.tot_w_herbivores == 22.8

    def test_move_check(self, example_herbivore):
        """
        A test that ensures that the boolean check_if_animal_moves behaves
        accordingly
        """
        random.seed(1)
        example_herbivore.phi = 1  # asserts probability of moving is high
        assert example_herbivore.movable()

    def test_migration(self, example_carnivore):
        cell1, cell2 = land.Savannah(), land.Savannah()
        cell1.pop["Carnivore"].append(example_carnivore)
        example_carnivore.move(cell1, cell2)
        assert len(cell2.pop["Carnivore"]) == 1

    def test_eat_in_order_fitness(self, example_savannah):
        herbert, herman = ani.Herbivore(), ani.Herbivore()
        herbert.weight, herbert.phi, herman.weight, herman.phi = 10, 10, 1, 0.5
        example_savannah.f = (herbert.param_dict['F'] - 1)
        example_savannah.pop['Herbivore'].append(herbert)
        example_savannah.pop['Herbivore'].append(herman)
        example_savannah.feeding()
        assert herbert.weight > herman.weight

    def test_check_kills(self, example_herbivore, example_carnivore):
        random.seed(999)
        example_herbivore.phi = 0.1
        example_carnivore.param_dict["DeltaPhiMax"] = 1
        # asserts that the probability of killing is high
        example_carnivore.phi = 1
        assert example_carnivore.check_if_kills(example_herbivore)

    def test_animal_dead(self, example_herbivore):
        example_herbivore.phi = 0
        assert example_herbivore.dies()

    def test_animal_dead_is_removed(self, example_herbivore, example_savannah):
        example_savannah.pop['Herbivore'].append(example_herbivore)
        example_herbivore.phi = 0
        example_savannah.dying()
        assert example_herbivore not in example_savannah.pop['Herbivore']

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
        old_parameter = example_carnivore.param_dict["w_birth"]
        example_carnivore.param_dict["w_birth"] = 10
        assert example_carnivore.param_dict["w_birth"] is not old_parameter

    def test_value_error_raised_placement_mountain_ocean(self):
        cell_mountain = land.Mountain()
        cell_ocean = land.Ocean()
        with pytest.raises(ValueError):
            cell_mountain.pop['Herbivore'].append(ani.Herbivore) and \
                cell_ocean.pop['Herbivore'].append(ani.Herbivore)

    def test_kill_order_fitness(self):
        cell = land.Jungle()
        herb, herman = ani.Herbivore(), ani.Herbivore()
        herb.phi, herman.phi = 0.4, 0.3
        killer, killer.phi = ani.Carnivore(), 1.0
        cell.pop.add(herb, herman, killer)
        isl.Island().feeding()
        assert cell.pop == 2


class TestRun:
    def test_do_collectively(self):
        pass

    def test_one_cycle(self):
        r = run.Run()
        r.one_cycle()
        assert r.years == 1

    def test_run(self):
        t = run.Run()
        t.run()
        assert t.years == t.desired_years

    def test_kill_check(mocker):
        mocker.patch('random.random', return_value=0.001)
        h = ani.Herbivore({'phi': 0.2})
        c1 = ani.Carnivore({'phi': 0.9})
        c2 = ani.Carnivore({'phi': 0.2})
        c3 = ani.Carnivore({'phi': 0.1})
        assert c1.check_if_kills(h)
        assert not c2.check_if_kills(h)
        assert not c3.check_if_kills(h)


class TestSimulation:
    def test_animal_distribution(self):
        sim.animal_distribution.get
        pass
