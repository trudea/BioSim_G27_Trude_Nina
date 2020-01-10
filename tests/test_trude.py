
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

    def test_savannah_instance(self):
        savannah = bs.Island(rossum_string)
        assert isinstance(savannah, bs.Island)