def num_to_coord(self, cols, num):
    x, y = 0, 0
    while num > cols:
        y += 1
        num -= cols
    x = num
    return (y, x)  # y før x


def coord_to_num(self, cols, y, x):  # y før x
    return y * cols + x


"""
class Island:
    def __init__(self, txt=None):
        if txt is None:
            txt = open('rossum.txt').read()
            if txt[-1] == "\n":
                #legg inn noe som fjerner siste element
                pass
        if txt[-1] is not "\n":
            print(len(txt))
            txt += "\n"
            print(len(txt))
        land_dict = {'S': Savannah, 'J': Jungle,
                     'O': Ocean, 'M': Mountain, 'D': Desert}
        line, lines = [], []
        y, x = 0, 0
        for letter in txt:
            if letter in land_dict:
                line.append(land_dict[letter](x, y))
                x += 1
            if letter == "\n":
                lines.append(line)
                line = []
                y += 1
                x = 0
        self.map = np.asarray(lines)

        left_column = [line[0] for line in self.map]
        right_column = [line[-1] for line in self.map]
        to_check = [self.map[0], self.map[-1], left_column, right_column]
        for list in to_check:
            for element in list:
                if not isinstance(element, Ocean):
                    raise ValueError
"""