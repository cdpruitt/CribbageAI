#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

with open("results.txt") as f:
    data = f.read()

x, y, z, dummy = np.loadtxt('results.txt').T

m = np.zeros([13, 13])

indices = np.triu_indices(13)

m[indices] = z

mask = np.tri(m.shape[0], k=-1)
m = np.ma.array(m, mask=mask)

fig = plt.figure()

ax = fig.add_subplot(1,1,1)
cmap = plt.cm.get_cmap('jet_r', 10)
cmap.set_bad('w')
ax.set_aspect('equal')
plt.imshow(m, interpolation='nearest', cmap=cmap)
plt.colorbar()

cardLabels = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
plt.xticks(range(len(cardLabels)), cardLabels)
plt.yticks(range(len(cardLabels)), cardLabels)

ax.xaxis.tick_top()

plt.show()

#m = np.triu(np.arange(0, 91, dtype=np.float).reshape(13, 13))

#matrix = z.reshape((13,13))

#plt.imshow(grid, extent=(x.min(), x.max(), y.max(), y.min()))
#
#plt.show()
