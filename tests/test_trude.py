
import BioSim_G27_Trude_Nina.src.biosim.island as isl
import BioSim_G27_Trude_Nina.src.biosim.animals as ani
import BioSim_G27_Trude_Nina.src.biosim.landscapes as land
import BioSim_G27_Trude_Nina.src.biosim.run as run

import pytest


class TestMap:
    def test_line_amount(self):
        pass


class Testanimal:

    def test_get_position(self):
        pass

    def test_place_animal(self):
        input = [{'loc': (3, 4), 'pop': [
            {'species': 'Herbivore', 'age': 10, 'weight': 12.5},
            {'species': 'Herbivore', 'age': 9, 'weight': 10.3}]}]

        i = bs.Island()
        i.place_animals(input)
        herbivore_list = i.island[3][4].herb.pop[1]
        assert type(herbivore_list).__name__ == 'Herbivore'

    def test_check_animal_in_cell(self):
        pass


    def test_move_animal(self):
        pass

    def test_eat_herbivore(self):
        pass

    def test_eat_in_order_fitness(self):
        pass

    def test_animal_dead(self):
        pass

    def test_parameter_change(self):
        pass

    def test_value_error_raised_placement_mountain_ocean(self):
        pass

    def test_die_order_fitness(self):
        pass
