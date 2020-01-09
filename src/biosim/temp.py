from math import exp

txt_str = open('rossum.txt').read()
string = txt_str.replace("\n", "")

class Animal:
    def __init__(self, age):
        self.age = age

    def set_weight(self):
        self.weight = 33

class Herbivore(Animal):
    def __init__(self, age):
        super().__init__(age)


if __name__ == "__main__":
    h = Herbivore(22)
    print(h.age)
    h.set_weight()
    print(type(h))
    print(exp(1))