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
    print
    d = {'eple' : 1, 'banan' : 2}
    for i in d:
        exec("self.%s = %s" % (i, d[i]))
    print(eple, banan)