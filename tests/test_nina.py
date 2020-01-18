import pytest
import src.biosim.animals as ani
import src.biosim.landscapes as land
import src.biosim.simulation as sim

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



@pytest.fixture
def ex_herbivores():
    yield [ani.Herbivore({'phi': 0.1}), ani.Herbivore({'phi': 0.5}),
     ani.Herbivore({'phi': 0.9})]

@pytest.fixture
def ex_carnivores():
    yield [ani.Carnivore({'phi': 0.1}), ani.Carnivore({'phi': 0.5}),
                  ani.Carnivore({'phi': 0.9})]

@pytest.fixture
def ex_savannah():
    yield land.Savannah()

def test_kill_check(mocker, ex_herbivores, ex_carnivores):
    mocker.patch('random.random', return_value=0.001)
    # h = ani.Herbivore({'phi': 0.5})
    h = ex_herbivores[1]
    c1 = ex_carnivores[0]
    c2 = ex_carnivores[1]
    c3 = ex_carnivores[2]
    assert not c1.check_if_kills(h)
    assert not c2.check_if_kills(h)
    assert c3.check_if_kills(h)

def test_feed_carnivore_weight_phi_change(mocker, ex_herbivores, ex_carnivores, ex_savannah):
    cell = ex_savannah
    mocker.patch('random.random', return_value=0.9)  # lavere enn sanns?
    cell.pop['Herbivore'] = ex_herbivores
    c1 = ani.Carnivore()
    former_weight = c1.weight
    former_phi = c1.phi
    c1.feeding(cell)
    assert c1.weight == former_weight
    assert c1.phi == former_phi
    mocker.patch('random.random', return_value=0.001)
    c2 = ani.Carnivore()
    former_weight = c2.weight
    c2.feeding(cell)
    assert c2.weight > former_weight
    assert former_phi < c2.phi


def test_feed_carnivore_pop_change(mocker, ex_savannah, ex_herbivores, ex_carnivores):
    cell = ex_savannah()
    mocker.patch('random.random', return_value=0.9) # lavere enn sanns?
    cell.pop['Herbivore'] = ex_herbivores
    c2.feeding(cell)
    assert len(cell.pop['Herbivore']) == 3
    mocker.patch('random.random', return_value=0.001)
    c2 = ani.Carnivore({'phi': 0.5})
    c2.feeding(cell)
    assert len(cell.pop['Herbivore']) == 0




def test_herbivore_weight():
    sim = BioSim()
    for cell in sim.map.values():
        for herbivore in cell.pop['Herbivore']:
            if herbivore.weight <= 0:
                assert False













