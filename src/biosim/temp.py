from math import exp
import numpy as np
class Savannah:
    pass

class Jungle:
    pass
class Mountain:
    pass
class Desert:
    pass
class Ocean:
    pass

land_dict = {'S' : Savannah, 'J': Jungle,
                    'O' : Ocean, 'M' : Mountain, 'D' : Desert}
txt = open('rossum.txt').read()
line, lines = [], []
x, y = 0, 0
for letter in txt:
    if letter in land_dict:
        line.append(letter)
        x += 1
    if letter == "\n":
        lines.append(line)
        line = []
        y += 1

print(len(lines[0]))


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
        def __init__(self, liv):
           self.a = 1
           self.c = self.a + self.b
           self.liv = liv
            # ønsker å ha en oppdater parametere-funksjon her. Må hente fra dict fra b

    class B(A):
        def __init__(self, liv):
            self.b = 2
            super().__init__(liv)
            #må sende inn alt som har blitt definert i underklassen

    klasse = B

    line = []
    lines = []


