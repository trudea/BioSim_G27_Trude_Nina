
import biosim.island as isl
import biosim.animals as ani
import biosim.landscapes as land
import biosim.run as run

import pytest

# keyword argument sorted
def get_propensity(self, animal, rel_abund):
    return exp(animal.lambdah * rel_abund)


"""
class AdjacentCell(Cell):
    total_propensity = 0
    total_probability = 0
    remembered_limit = 0

    def __init__(self, y, x, letter):
        super().__init__(y, x, letter)
        self.propensity = None
        self.probability = None
        self.lower_limit = 0
        self.upper_limit = 0
"""


class TestMap:
    def test_line_amount(self):
        pass

    def test_num_specimen(self):
        pass

    def test_choose_new_cell(self):
        pass


class Testanimal:

    def test_move_check(self):
        pass

    def test_check_procreation(self):
        pass

    def test_check_kills(self):
        pass


class TestRun:
    def test_collective_replenishing(self):
        pass

    def test_collective_feeding(self):
        pass

    def test_collective_procreation(self):
        pass

    def test_run(self):
        pass

    def test_one_cycle(self):
        pass
