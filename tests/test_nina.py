import pytest
import src.biosim.run as bs
import src.biosim.island as isl
import src.biosim.animals as ani
import src.biosim.landscapes as land

class TestIsland:
    rossum_string = 'OOOOOOOOOOOOOOOOOOOOO\nOSSSSSJJJJMMJJJJJJJOO\nOSSSSSJJJJMMJJJJJJJOO\nOSSSSSJJJJMMJJJJJJJOO\nOOSSJJJJJJJMMJJJJJJJO\nOOSSJJJJJJJMMJJJJJJJO\nOOOOOOOSMMMMJJJJJJJJO\nOSSSSSJJJJMMJJJJJJJOO\nOSSSSSSSSSMMJJJJJJOOO\nOSSSSSDDDDDJJJJJJJOOO\nOSSSSSDDDDDJJJJJJJOOO\nOSSSSSDDDDDJJJJJJJOOO\nOSSSSSDDDDDMMJJJJJOOO\nOSSSSSDDDDDJJJJOOOOOO\nOOSSSDDDDDDJJOOOOOOOO\nOOSSSSDDDDDDJJOOOOOOO\nOSSSSSDDDDDJJJJJJJOOO\nOSSSSDDDDDDJJJJOOOOOO\nOOSSSSDDDDDJJJOOOOOOO\nOOOSSSSJJJJJJJOOOOOOO\nOOOSSSSSSOOOOOOOOOOOO\nOOOOOOOOOOOOOOOOOOOOO'

    def test_construct_island(self):
        rossum_string = 'OOOOOOOOOOOOOOOOOOOOO\nOSSSSSJJJJMMJJJJJJJOO\nOSSSSSJJJJMMJJJJJJJOO\nOSSSSSJJJJMMJJJJJJJOO\nOOSSJJJJJJJMMJJJJJJJO\nOOSSJJJJJJJMMJJJJJJJO\nOOOOOOOSMMMMJJJJJJJJO\nOSSSSSJJJJMMJJJJJJJOO\nOSSSSSSSSSMMJJJJJJOOO\nOSSSSSDDDDDJJJJJJJOOO\nOSSSSSDDDDDJJJJJJJOOO\nOSSSSSDDDDDJJJJJJJOOO\nOSSSSSDDDDDMMJJJJJOOO\nOSSSSSDDDDDJJJJOOOOOO\nOOSSSDDDDDDJJOOOOOOOO\nOOSSSSDDDDDDJJOOOOOOO\nOSSSSSDDDDDJJJJJJJOOO\nOSSSSDDDDDDJJJJOOOOOO\nOOSSSSDDDDDJJJOOOOOOO\nOOOSSSSJJJJJJJOOOOOOO\nOOOSSSSSSOOOOOOOOOOOO\nOOOOOOOOOOOOOOOOOOOOO'
        i = bs.Island(rossum_string)
        assert isinstance(i, bs.Island)


    def test_construct_savannah(self):
        s = isl.Savannah()
        assert isinstance(s, isl.Savannah)


    def test_place_animals(self):
        simple_island_string = 'OOOOO\nOSSSO\nOSSSO\nOSSSO\nOOOOO'
        i = bs.Island(simple_island_string)


    def test_check_edges(self):
        """
        A test that checks if ValueError is raised if there are no ocean
        tiles surrounding the island.
        """
        with pytest.raises(ValueError):
            isl.Island('OSO\nOSO\nOOO')
        with pytest.raises(ValueError):
            isl.Island('OO\nJSO\nOOO')
        with pytest.raises(ValueError):
            isl.Island('OO\nOSJ\nOOO')
        with pytest.raises(ValueError):
            isl.Island('OO\nOSO\nJOO')

def test_kill_check(mocker):
    mocker.patch('random.random', return_value=0.001)
    h = ani.Herbivore({'phi': 0.2})
    c1 = ani.Carnivore({'phi': 0.9})
    c2 = ani.Carnivore({'phi': 0.2})
    c3 = ani.Carnivore({'phi': 0.1})
    assert c1.check_if_kills(h)
    assert not c2.check_if_kills(h)
    assert not c3.check_if_kills(h)

def test_carnivore_feeding(mocker):
    cell = land.Savannah()
    mocker.patch('random.random', return_value=0.001) # lavere enn sanns?
    cell.pop['Herbivore'] = [ani.Herbivore({'phi': 0.1}), ani.Herbivore({'phi': 0.5}), ani.Herbivore({'phi': 0.9})]
    c1 = ani.Carnivore({'phi: ', 0.01})
    c1.feed
    c2 = ani.Carnivore({'phi': 0.5})
    c2.feeding(cell, cell.pop['Herbivore'])
    assert len(cell.pop['Herbivore']) == 0





