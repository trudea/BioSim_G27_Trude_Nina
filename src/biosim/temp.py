from math import exp
import numpy as np

txt = open('rossum.txt').read()


class Animal:
    def __init__(self, age):
        self.age = age

    def set_weight(self):
        self.weight = 33

class Herbivore(Animal):
    def __init__(self, age):
        super().__init__(age)


if __name__ == "__main__":
    dict = {'banan' : 1, 'eple' : 2}
    dict2 = dict.copy()
    dict2['banan'] = 3
    print(dict)
