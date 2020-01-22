import src.biosim.animals as animals
import pytest


class BaseTestAnimal:
    AnimalType = animals.Animal

    @pytest.fixture
    def ex_ani(self):
        yield self.AnimalType()

    def test_isinstance(self, ex_ani):
        assert isinstance(ex_ani, animals.Animal)

    def test_set_params(self, ex_ani):
        different_params = {'a_half': 123, 'gamma': 456 }
        ex_ani.set_params(different_params)
        assert ex_ani.a_half == 123
        assert ex_ani.gamma == 456

    def test_initial_age(self, ex_ani):
        assert ex_ani.age == 0

    def test_aging(self, ex_ani):
        ex_ani.aging()
        ex_ani.aging()
        assert ex_ani.age == 2

    def test_phi(self, ex_ani):
        assert 0 < ex_ani.phi < 1

    def test_weightloss(self, ex_ani):
        remembered_w = ex_ani.weight
        ex_ani.weightloss()
        assert 0 <= ex_ani.weight < remembered_w

    def test_dying(self, mocker, ex_ani):
        mocker.patch('np.random.random', return_value=0.999)
        dying_animal = ex_ani
        dying_animal.weight = 0
        survivor = ex_ani
        print(survivor.weight)
        assert dying_animal.dies == True
        mocker.patch('np.random.random', return_value=0.999)
        assert survivor.dies == False



class TestHerbivore(BaseTestAnimal):
    AnimalType = animals.Herbivore



