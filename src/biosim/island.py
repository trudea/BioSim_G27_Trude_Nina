class Landscape:
    def __init__(self, txt_str=None):
        if txt_str is None:
            txt_str = open('rossum.txt').read()
            # txt_str = txt_str.split() # liste med tekststrenger
            map_str = txt_str.replace("\n", "") #  en lang streng
        self.map_string = map_str
        self.map_dict = {}
        self.cols = 21 # må endres
        self.savannah = []
        self.jungle = []
        self.desert = []
        self.mountain = []
        self.ocean = []
        for n, i in enumerate(self.map_string):
            map_dict[num_to_cord] = [i]
            if i == 'S':
                self.savannah.append(n)
            if i == 'J':
                self.jungle.append(n)
            if i == 'D':
                self.desert.append(n)
            if i == 'M':
                self.mountain.append(n)

    def num_to_coord(self, cols, num):
        x = 0
        y = 0
        while num > cols:
            y += 1
            num -= cols
        x = num
        return y, x

    def coord_to_num(self, cols, x, y):
        num = y*cols + x

    def new_position(self):
        #when animal moves, this gives new position
        pass

    def growing(self):
        pass

class Savannah(Landscape):
    default_param_dict = {'f_max' : 300.0}
    savannah = []
    savannah_dict = {}

    def __init__(self, map_string, num, param_dict=None):
        self.map_string = map_string
        for n, i in enumerate(self.map_string):
            if i == 'S':
                self.coords.append(n)
                savannah_dict[(num_to_coords(n))] = 0
        if param_dict is None: # burde sannsynligvis være i superklassen
            self.param_dict = default_param_dict
        else:
            for i in default_param_dict:
                if i not in param_dict:
                    param_dict[i] = default_param_dict[i]



class Jungle(Landscape):
    default_param_dict = {'f_max' : 800.0, 'alpha' : 0.3}

    def __init__(self, island, param_dict):
        self.island = island
        if param_dict is None:
            self.param_dict = default_param_dict
        else:
            for i in default_param_dict:
                if i not in param_dict:
                    param_dict[i] = default_param_dict[i]


class Animal:
    def __init__(self, island):
        self.island = island
        self.position

    def feeding(self):
        pass

    def procreation(self):
        pass

    def migration(self):
        pass

    def aging(self):
        pass

    def weightloss(self):
        pass


class Herbivore(Animal):
    default_param_dict = {'w_birth': 8.0,
                          'sigma_birth': 1.5,
                          'beta': 0.9,
                          'eta': 0.05,
                          'a_half': 40.0,
                          'phi_age': 0.2,
                          'w_half': 10.0,
                          'phi_weight': 0.1,
                          'mu': 0.25,
                          'lambda': 1.0,
                          'gamma': 0.2,
                          'zeta': 3.5,
                          'xi': 1.2,
                          'omega': 0.4,
                          'F': 10.0
                          }

    def __init__(self, island, param_dict):
        super().__init__(island)
        # bør default_param_dict stå utenfor definisjonen?
        if param_dict is None:
            self.param_dict = default_param_dict
        else:
            for i in default_param_dict:
                if i not in param_dict:
                    param_dict[i] = default_param_dict[i]
        self.param_dict = param_dict

class Carnivore(Animal):
    default_param_dict = {'w_birth': 6.0,
                          'sigma_birth': 1.0,
                          'beta': 0.75,
                          'eta': 0.125,
                          'a_half': 60.0,
                          'phi_age': 0.4,
                          'w_half': 4.0,
                          'phi_weight': 0.4,
                          'mu': 0.4,
                          'lambda': 1.0,
                          'gamma': 0.8,
                          'zeta': 3.5,
                          'xi': 1.1,
                          'omega': 0.9,
                          'F': 50.0,
                          'DeltaPhiMax' : 10.0
                          }

    def __init__(self, island, param_dict):
        super().__init__(island)
        if param_dict is None:
            self.param_dict = default_param_dict
        else:
            for i in default_param_dict:
                if i not in param_dict:
                    param_dict[i] = default_param_dict[i]
        self.param_dict = param_dict

    def check_if_kills(self):
        pass

class Simulation:
    def __init__(self):
        pass

    def single_run(self):
        first_island = Island()
        first_herbivores = []
        first_carnivores = []
        for _ in range(initial_num_of_herbivores):
            first_herbivores.append(Herbivore()) # legger ny instance til liste
        for _ in range(initial_num_of_carnivores):
            first_carnivores.append(Carnivore())

if __name__ == "__main__":
    fir