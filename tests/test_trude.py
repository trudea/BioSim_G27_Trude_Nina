
import BioSim_G27_Trude_Nina.src.biosim.island as bs
import pytest


class TestIsland:

    def test_constructor_default(self):
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

    def test_map_ocean(self):
        with pytest.raises(ValueError):
            bs.Island('SSS\nOOO')
            bs.Island('OOO\nOSS')
            bs.Island('OOO\nOSO\nOSO')

    def test_jungle_instance(self):
        jungle = bs.Jungle(None, None)
        assert isinstance(jungle, bs.Jungle)

    def test_desert_instance(self):
        desert = bs.Desert(None, None)
        assert isinstance(desert, bs.Desert)

    def test_ocean(self):
        ocean = bs.Ocean(None, None)
        assert isinstance(ocean, bs.Ocean)

    def test_mountain(self):
        mountain = bs.Mountain(None, None)
        assert isinstance(mountain, bs.Mountain)

    def test_fodder_savannah(self):
        savannah = bs.Savannah(None, None)
        savannah.f = 200
        savannah.replenish()
        assert savannah.f > 200

    def test_fodder_jungle(self):
        jungle = bs.Jungle(None, None)
        jungle.f = 500
        jungle.replenish()
        assert jungle.f == jungle.param_dict['f_max']


class TestAnimal:

    def test_herbivore(self):
        herbivore = bs.Herbivore(None, None, None)
        assert isinstance(herbivore, bs.Herbivore)

    def test_carnivore(self):
        carnivore = bs.Carnivore(None, None, None)
        assert isinstance(carnivore, bs.Carnivore)

    def test_aging(self):
        herbivore = bs.Herbivore(None, None, None)
        age = herbivore.age
        herbivore.aging()
        assert herbivore.age > age

    def test_weightloss(self):
        herbivore = bs.Herbivore(None, None, None)
        weight = herbivore.weight
        herbivore.weightloss()
        assert herbivore.weight < weight

    def test_herbivore_feeding(self):
        herbivore = bs.Herbivore(None, None, None)
        weight = herbivore.weight
        F = herbivore.param_dict['F']
        herbivore.feeding(F)
        assert weight < herbivore.weight
