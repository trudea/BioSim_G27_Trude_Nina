# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

# -*- coding: utf-8 -*-

"""
"""

__author__ = "Trude Haug Almestrand", "Nina Mariann Vesseltun"
__email__ = "trude.haug.almestrand@nmbu.no", "nive@nmbu.no"

import numpy as np
from math import exp
import random

class Landscape:
    def __init__(self):
        pass


class Savannah(Landscape):
    param_dict = {'f_max' : 300.0, 'alpha' : 0.3}

    def __init__(self, param_dict=None):
        super().__init__()
        if param_dict is not None:
            self.param_dict.update(param_dict)
        for parameter in self.param_dict:
            exec("self.%s = %s" % (parameter, self.param_dict[parameter]))
        self.f = self.f_max
        # self.herbivores_in_cell = [first_herbivores[0], first_herbivores[1]]

    def replenish(self):
        self.f += self.alpha * (self.f_max - self.f)



class Jungle(Landscape):
    param_dict = {'f_max' : 800.0}

    def __init__(self, param_dict=None):
        super().__init__()
        if param_dict is not None:
            self.param_dict.update(param_dict)
        for parameter in self.param_dict:
            exec("self.%s = %s" % (parameter, self.param_dict[parameter]))
        self.f = self.f_max

    def replenish(self):
        self.f = self.f_max


class Desert(Landscape):
    def __init__(self):
        super().__init__()
        self.f = 0


class Ocean(Landscape):
    def __init__(self):
        super().__init__()


class Mountain(Landscape):
    def __init__(self):
        super().__init__()

