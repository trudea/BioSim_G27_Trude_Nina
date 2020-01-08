class Island:
    def __init__(self, txt_str=None):
        if txt_str is None:
            txt_str = open('rossum.txt').read()
            txt_str = txt_str.split()
        self.landscape = txt_str # liste med tekststrenger

class Landscape:
    def __init__(self):
        pass

    def growing(self):
        pass

class Savannah(Landscape):
    def __init__(self, f_max=300.0):
        self.f_max = f_max

class Jungle(Landscape):
    def __init__(self, f_max=800.0, alpha=0.3):
        self.f_max = f_max
        self.alpha = 0.3

class Animal:
    def __init__(self):
        self.param_dict = {'lambda': 1.0, 'zeta' = 3.5}

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
    def __init__(self, param_dict):
        if param_dict is None:
            param_dict = {'w_birth' : 8.0,
                 'sigma_birth' : 1.5,
                  'beta' : 0.9,
                  'eta': 0.05,
                  'a_half' : 40.0,
                  'phi_age' : 0.2,
                  'w_half' : 10.0,
                  'phi_weight' : 0.1,
                  'mu' : 0.25,
                  'lambda' : 1.0,
                  'gamma' : 0.2,
                  'zeta' : 3.5,
                  'xi' : 1.2,
                  'omega' : 0.4,
                  'F' : 10.0
                  }
        self.param_dict = param_dict

class Carnivore(Animal):
    def __init__(self, param_dict):
        if param_dict is None:
            self.param_dict = {'w_birth': 6.0,
                   'sigma_birth': 1.0,
                   'beta': 0.75,
                   'eta': 0.125,
                   'a_half': 60.0,
                   'phi_age': 0.4,
                   'w_half': 4.0,
                   'phi_weight' : 0.4,
                   'mu': 0.4,
                   'lambda': 1.0,
                   'gamma': 0.8,
                   'zeta': 3.5,
                   'xi': 1.1,
                   'omega': 0.9,
                   'F': 50.0
                   'DeltaPhiMax' : 10.0
                   }

    def check_if_kills(self):
        pass