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
    for i in range(3):
        print(a[i][0])
    # print(a[:][0])
    test = [liste[0] for liste in a]
    print(test)