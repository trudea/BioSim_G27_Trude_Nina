def num_to_coord(self, cols, num):
    x, y = 0, 0
    while num > cols:
        y += 1
        num -= cols
    x = num
    return (y, x)  # y før x


def coord_to_num(self, cols, y, x):  # y før x
    return y * cols + x