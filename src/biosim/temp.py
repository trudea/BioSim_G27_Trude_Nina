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


class Animal:
    def __init__(self):
        self.phi = None

    def set_weight(self):
        self.weight = 33

class Herbivore(Animal):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    def bubble_sort(datavariable):
        copy = list(datavariable)
        for i in range(len(copy) - 1):
            for j in range(len(copy) - i - 1):
                if copy[j] > copy[j + 1]:
                    copy[j], copy[j + 1] = copy[j + 1], copy[j]
        return copy

    #et element er en instans, må sorteres etter element.phi

    test = []
    def bubble_sort_animals(original_order):
        copy = list(original_order)
        for i in range(len(copy) - 1):
            for j in range(len(copy) - i - 1):
                if copy[j].phi < copy[j + 1].phi:
                    copy[j], copy[j + 1] = copy[j + 1], copy[j]
        return copy

    herman = Herbivore()
    herbert = Herbivore()
    hermine = Herbivore()
    herman.phi = 0.3
    herbert.phi = 0.1
    hermine.phi = 0.5
    test_liste=[herman, herbert, hermine]
    new_animal_order = bubble_sort_animals(test_liste)
    for i in new_animal_order:
        print(i.phi)



