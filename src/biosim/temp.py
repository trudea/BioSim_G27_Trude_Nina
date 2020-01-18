class Country:
    def __init__(self):
        self.name = 'Montenegro'
        self.food = ['eple', 'pære', 'banan']

    @property
    def num_food(self):
        return self._num_food

    @num_food.getter
    def num_food(self, x):
        if x == 1:
            self._num_food = len(self.food)
        elif x == 2:
            self._num_food = 44


d = Country()
d.num_food() = 5
print(d.num_food())