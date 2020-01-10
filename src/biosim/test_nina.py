import src.BioSim_G27_Trude_Nina.island as bs
import pytest

class TestIsland:

    def test_constructor_default_(self):
        i = bs.Island()
        assert isinstance(i, bs.Island)