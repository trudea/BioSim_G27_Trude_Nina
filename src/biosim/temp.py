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
    a = np.array([[1, 2],[3, 4]])
    print(a)
    print(a[0,1])

dictionary = { (0,0) :['first_herbivore', 'second_herbivore']}
print(a)

