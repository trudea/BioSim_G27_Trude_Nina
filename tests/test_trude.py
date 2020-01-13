
import BioSim_G27_Trude_Nina.src.biosim.island as isl
import BioSim_G27_Trude_Nina.src.biosim.animals as ani
import BioSim_G27_Trude_Nina.src.biosim.landscapes as land
import BioSim_G27_Trude_Nina.src.biosim.run as run
import pytest
import random


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

if __name__ == "__main__":
    cell = isl.Cell(3, 3, 'S')
    island = isl.Island()
    carnivore1, carnivore2 = ani.Carnivore(), ani.Carnivore()
    carnivore1.weight, carnivore1.phi = 15, 1
    carnivore2.weight, carnivore2.phi = 15, 1
    cell.pop.append([carnivore1, carnivore2])
    print(cell.pop)