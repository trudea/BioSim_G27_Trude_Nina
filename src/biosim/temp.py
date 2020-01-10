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
    a = np.array([[1, 2, 3], [3, 4, 5],[6, 7, 8]])
    liste = [[1, 2, 3], [3, 4, 5], [6, 7, 8]]

    class A:
        def __init__(self):
           self.a = 1
           self.c = self.a + self.b
            # ønsker å ha en oppdater parametere-funksjon her. Må hente fra dict fra b

    class B(A):
        def __init__(self):
            self.b = 2
            super().__init__()
            #må sende inn alt som har blitt definert i underklassen

    are = B()
    print(are.c)