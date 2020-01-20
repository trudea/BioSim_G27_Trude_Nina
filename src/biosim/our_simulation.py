import pandas as pd
import random

xy = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
data = [random.randint(0, 100) for i in range(9)]

x = []
y = []
lines = 0
for tuples in xy:
    if tuples[0] in y:
        y.append(tuples[0])
        lines += 1
    if tuples[1] in x:
        x.append(tuples[1])

dat = pd.DataFrame(data)
print(x, y, lines)