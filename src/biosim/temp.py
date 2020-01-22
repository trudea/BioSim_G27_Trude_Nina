import src.biosim.animals as animals
import pytest
import numpy as np


class BaseTestAnimal:
    AnimalType = animals.Animal

    @pytest.fixture
    def ex_ani(self):
        yield self.AnimalType()

    @pytest.fixture
    def ex_fit_ani(self):
        ani = self.AnimalType()
        ani.weight = 90
        yield ani

    @pytest.fixture
    def ex_unfit_ani(self):
        ani = self.AnimalType()
        ani.weight = 0
        yield ani

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

    def test_dying(self, mocker, ex_fit_ani, ex_unfit_ani):
        mocker.patch('np.random.random', return_value=0)
        survivor = ex_fit_ani
        assert survivor.dies() is False
        mocker.patch('np.random', return_value=1)
        dying_ani = ex_unfit_ani
        assert dying_ani.dies()

    def test_movable(self, mocker, ex_fit_ani, ex_unfit_ani):
        mocker.patch('np.random.random', return_value=0)
        fit_ani = ex_fit_ani
        assert fit_ani.movable()
        mocker.patch('np.random', return_value=1)
        unfit_ani = ex_fit_ani
        assert unfit_ani.movable() is False

    def test_get_relabundance(self):






class TestHerbivore(BaseTestAnimal):
    AnimalType = animals.Herbivore



