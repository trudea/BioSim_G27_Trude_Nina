import pytest
import src.biosim.animals as ani
import src.biosim.landscapes as land
import src.biosim.simulation as sim

"""
class TestIsland:
    rossum_string = 'OOOOOOOOOOOOOOOOOOOOO\nOSSSSSJJJJMMJJJJJJJOO\nOSSSSSJJJJMMJJJJJJJOO\nOSSSSSJJJJMMJJJJJJJOO\nOOSSJJJJJJJMMJJJJJJJO\nOOSSJJJJJJJMMJJJJJJJO\nOOOOOOOSMMMMJJJJJJJJO\nOSSSSSJJJJMMJJJJJJJOO\nOSSSSSSSSSMMJJJJJJOOO\nOSSSSSDDDDDJJJJJJJOOO\nOSSSSSDDDDDJJJJJJJOOO\nOSSSSSDDDDDJJJJJJJOOO\nOSSSSSDDDDDMMJJJJJOOO\nOSSSSSDDDDDJJJJOOOOOO\nOOSSSDDDDDDJJOOOOOOOO\nOOSSSSDDDDDDJJOOOOOOO\nOSSSSSDDDDDJJJJJJJOOO\nOSSSSDDDDDDJJJJOOOOOO\nOOSSSSDDDDDJJJOOOOOOO\nOOOSSSSJJJJJJJOOOOOOO\nOOOSSSSSSOOOOOOOOOOOO\nOOOOOOOOOOOOOOOOOOOOO'

    def test_construct_island(self):
        rossum_string = 'OOOOOOOOOOOOOOOOOOOOO\nOSSSSSJJJJMMJJJJJJJOO\nOSSSSSJJJJMMJJJJJJJOO\nOSSSSSJJJJMMJJJJJJJOO\nOOSSJJJJJJJMMJJJJJJJO\nOOSSJJJJJJJMMJJJJJJJO\nOOOOOOOSMMMMJJJJJJJJO\nOSSSSSJJJJMMJJJJJJJOO\nOSSSSSSSSSMMJJJJJJOOO\nOSSSSSDDDDDJJJJJJJOOO\nOSSSSSDDDDDJJJJJJJOOO\nOSSSSSDDDDDJJJJJJJOOO\nOSSSSSDDDDDMMJJJJJOOO\nOSSSSSDDDDDJJJJOOOOOO\nOOSSSDDDDDDJJOOOOOOOO\nOOSSSSDDDDDDJJOOOOOOO\nOSSSSSDDDDDJJJJJJJOOO\nOSSSSDDDDDDJJJJOOOOOO\nOOSSSSDDDDDJJJOOOOOOO\nOOOSSSSJJJJJJJOOOOOOO\nOOOSSSSSSOOOOOOOOOOOO\nOOOOOOOOOOOOOOOOOOOOO'
        i = bs.Island(rossum_string)
        assert isinstance(i, bs.Island)


    

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


"""
class TestSimulation:
    @pytest.fixture
    def big_map(self):
        return """OOOOO\nOJJJO\nOJJJO\nOJJJO\nOOOOO"""


    @pytest.fixture
    def herb_tribe(self):
        herb_list = [{'species': 'Herbivore', 'age': 6, 'weight': 20} for i in range(3)]
        yield herb_list


    @pytest.fixture
    def carn_tribe(self):
        carn_list = [{'species': 'Carnivore', 'age': 6, 'weight': 20} for i in range(3)]
        yield carn_list


    @pytest.fixture
    def both_species(self, herb_tribe, carn_tribe):
        both = herb_tribe.copy()
        both.append(carn_tribe)
        yield both


    @pytest.fixture
    def big_sim(self, big_map, herb_tribe):
        big_sim = sim.BioSim(big_map, [{'loc': (2,2), 'pop': herb_tribe}], 123)
        yield big_sim

    def test_place_herbivores(self, big_sim):
        cell = big_sim.map[(2,2)]
        assert len(cell.pop) == 2
        assert len(cell.pop['Herbivore']) == 3
        assert len(cell.pop['Carnivore']) == 0

    def test_place_carnivores(self, big_sim, carn_tribe):
        new_pop = [{'loc': (2,2), 'pop': carn_tribe}]
        cell = big_sim.map[(2, 2)]
        big_sim.add_population(new_pop)
        assert len(cell.pop) == 2
        assert len(cell.pop['Herbivore']) == 3
        assert len(cell.pop['Carnivore']) == 3

    @pytest.fixture(big_sim)
    def new_sim(self, big):
        


    def test_num_animals(self, big_sim, carn_tribe):
        new_pop = [{'loc': (2, 2), 'pop': carn_tribe}]
        cell = big_sim.map[(2, 2)]
        big_sim.add_population(new_pop)
        assert big_sim.num_animals == 6











