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
    def random_map(self):
        return 'OOOOO\nODJMO\nOJJSO\nOJSDO\nOOOOO'

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
    def jungle_sim(self, random_map, herb_tribe):
        jungle_sim = sim.BioSim(random_map, [{'loc': (2,2), 'pop': herb_tribe}], 123)
        yield jungle_sim


    def test_place_herbivores(self, jungle_sim, carn_tribe):
        cell = jungle_sim.map[(2,2)]
        assert len(cell.pop) == 2
        assert len(cell.pop['Herbivore']) == 3
        assert len(cell.pop['Carnivore']) == 0

    def test_place_carnivores(self, jungle_sim, carn_tribe):
        new_pop = [{'loc': (2,2), 'pop': carn_tribe}]
        cell = jungle_sim.map[(2, 2)]
        jungle_sim.add_population(new_pop)
        assert len(cell.pop) == 2
        assert len(cell.pop['Herbivore']) == 3
        assert len(cell.pop['Carnivore']) == 3


    @pytest.fixture
    def new_jungle_sim(self, jungle_sim, carn_tribe):
        new_pop = [{'loc': (2, 2), 'pop': carn_tribe}]
        jungle_sim.add_population(new_pop)
        yield jungle_sim


    def test_simple_num_animals(self, new_jungle_sim):
        assert new_jungle_sim.num_animals == 6
        assert len(new_jungle_sim.map[(2, 2)].pop['Herbivore']) +\
               len(new_jungle_sim.map[(2, 2)].pop['Carnivore']) == 6

    @pytest.fixture
    def island(self, new_jungle_sim):
        new_pop = [{'species': 'Carnivore', 'age': 6, 'weight': 20} for i in
                   range(2)]
        new_pop += [{'species': 'Herbivore', 'age': 6, 'weight': 20} for i in
                    range(4)]
        new_jungle_sim.add_population([{'loc': (2, 3), 'pop': new_pop}])
        yield new_jungle_sim

    def test_num_animals_two_cells(self, island):
        assert island.num_animals == 12

    def test_num_per_species(self, island):
        assert island.num_animals_per_species['Herbivore'] == 7
        assert island.num_animals_per_species['Carnivore'] == 5

    def test_animal_num_stable(self, island):
        remembered = island.num_animals_per_species
        rem_n = island.num_animals
        island.all_cells('replenish')
        assert  island.num_animals_per_species == remembered
        island.all_cells('feeding')
        assert  island.num_animals_per_species == remembered
        island.migration()
        assert  island.num_animals_per_species == remembered
        island.all_animals('aging')
        assert island.num_animals_per_species == remembered
        island.all_animals('weightloss')
        assert island.num_animals_per_species == remembered
        assert rem_n == island.num_animals

    @pytest.fixture
    def jungle(self):
        simple_map = 'OOO\nOJO\nOOO'
        yield sim.BioSim(simple_map)

    @pytest.fixture
    def savannah(self):
        simple_map = 'OOO\nOSO\nOOO'
        yield sim.BioSim(simple_map)

    @pytest.fixture
    def desert(self):
        simple_map = 'OOO\nODO\nOOO'
        yield sim.BioSim(simple_map)


    @pytest.fixture
    def mountain(self):
        simple_map = 'OOO\nOMO\nOOO'
        yield sim.BioSim(simple_map)

    @pytest.fixture
    def ocean(self):
        simple_map = 'OOO\nOOO\nOOO'
        yield sim.BioSim(simple_map)

    def test_feeding(self, savannah):
        herbivore = {'species': 'Herbivore', 'age': 5, 'weight': 20}
        savannah.add_population([{'loc': (1, 1), 'pop': [herbivore]}])
        savannah.all_cells('feeding')
        cell = savannah.map[(1,1)]
        assert cell.pop['Herbivore'][0].weight > 5

    def test_savannah_feeding(self, island):
        """Check if herbivores gain weight feeding on savannah, and if fodder
        runs out."""
        simple_map = 'OOO\nOSO\nOOO'
        herbivores =   [{'species': 'Herbivore', 'age': 5, 'weight': 20.0} for i in range(31)]
        island = sim.BioSim(simple_map, [{'loc': (1, 1), 'pop': herbivores}],
                            123)
        cell = island.map[(1, 1)]
        old_phi = [herbivore.phi for herbivore in cell.pop['Herbivore']]
        island.all_cells('feeding')
        for i, herbivore in enumerate(cell.pop['Herbivore'][0:-2]):
            assert cell.pop['Herbivore'][-2].weight > 20.0
            assert herbivore.phi > old_phi[i]
        assert cell.pop['Herbivore'][-1].weight == 20.0
        assert cell.pop['Herbivore'][-1].phi == old_phi[-1]


    def test_jungle_feeding(self, jungle):
        """Check if herbivores gain weight feeding in jungle, and if fodder
        runs out."""

        herbivores = [{'species': 'Herbivore', 'age': 5, 'weight': 20.0}
                      for i in range(81)]
        jungle.add_population([{'loc': (1, 1), 'pop': herbivores}])
        cell = jungle.map[(1, 1)]
        old_phi = [herbivore.phi for herbivore in cell.pop['Herbivore']]
        jungle.all_cells('feeding')
        for i, herbivore in enumerate(cell.pop['Herbivore'][0:-2]):
            assert herbivore.weight > 20.0
            assert herbivore.phi > old_phi[i]
        assert cell.pop['Herbivore'][-1].weight == 20.0
        assert cell.pop['Herbivore'][-1].phi == old_phi[-1]

    def test_desert_feeding(self, desert):
        """Check that herbivore doesn't gain weight in desert."""
        desert.add_population([{'loc': (1, 1), 'pop':
            [{'species': 'Herbivore', 'age': 5, 'weight': 20.0}]}])
        cell = desert.map[(1, 1)]
        old_phi = cell.pop['Herbivore'][0].phi
        desert.all_cells('feeding')
        assert cell.pop['Herbivore'][0].weight == 20.0
        assert cell.pop['Herbivore'][0].phi == old_phi


    def test_unsuitable_placements(self, mountain, ocean):
        """Check that population can't be placed on mountain or in the
        ocean."""
        with pytest.raises(ValueError):
            mountain.add_population([{'loc': (1, 1), 'pop':
                [{'species': 'Herbivore', 'age': 5, 'weight': 20}]}])
        with pytest.raises(ValueError):
            mountain.add_population([{'loc': (0, 0), 'pop':
                [{'species': 'Herbivore', 'age': 5, 'weight': 20}]}])

    def test_carnivore_feeding(self, desert, mocker):
        """Test if carnivore gains weight and increases fitness in cell with
        herbivores, and if herbivore population is diminished. """
        mocker.patch('random.random', return_value=0.0001)
        herb_pop = [{'species': 'Herbivore', 'age': 5, 'weight': 20} for i in range(200)]
        carn_pop = [{'species': 'Carnivore', 'age': 5, 'weight': 20}]
        ini_pop = herb_pop + carn_pop
        desert.add_population([{'loc': (1,1), 'pop': ini_pop}])
        cell = desert.map[(1, 1)]
        old_phi = cell.pop['Carnivore'][0].phi
        old_num_herbivores = len(cell.pop['Herbivore'])
        old_tot_w = cell.tot_w_herbivores
        desert.all_cells('feeding')
        assert cell.pop['Carnivore'][0].weight > 20
        assert cell.pop['Carnivore'][0].phi > old_phi
        assert len(cell.pop['Herbivore']) < old_num_herbivores
        assert cell.tot_w_herbivores < old_tot_w

    def test_carnivore_procreation(self, desert):
        """Test if carnivores are born"""
        carn_pop = [{'species': 'Carnivore', 'age': 5, 'weight': 20} for i in range(50)]
        desert.add_population([{'loc': (1,1), 'pop': carn_pop}])
        desert.all_cells('procreation')
        cell = desert.map[(1, 1)]
        assert len(cell.pop['Carnivore']) > 50








