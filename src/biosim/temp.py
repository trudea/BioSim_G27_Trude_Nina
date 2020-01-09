from math import exp
import numpy as np

txt = open('rossum.txt').read()

print(txt)

class Animal:
    def __init__(self, age):
        self.age = age

    def set_weight(self):
        self.weight = 33

class Herbivore(Animal):
    def __init__(self, age):
        super().__init__(age)


if __name__ == "__main__":
    print
    d = {'eple' : 1, 'banan' : 2}


    a = np.array([[1, 2],[3, 4]])
    c = [5, 6]
    b = list(a)
    b.append(c)
    a = np.asarray(b)
