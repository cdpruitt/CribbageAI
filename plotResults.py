#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

with open("results.txt") as f:
    data = f.read()

data = data.split('\n')

x = [row.split(' ')[0] for row in data]
y = [row.split(' ')[1] for row in data]
z = [row.split(' ')[2] for row in data]

matrix = z.reshape((13,13))

fig = plt.figure()
plt.imshow(grid, extent=(x.min(), x.max(), y.max(), y.min()))

plt.show()
