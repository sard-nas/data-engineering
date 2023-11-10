import numpy as np
import os

matrix = np.load('matrix_74_2.npy')
size = len(matrix)
lim = 574
x, y, z = [], [], []

for i in range(size):
    for j in range(size):
        if matrix[i][j] > lim:
            x.append(i)
            y.append(j)
            z.append(matrix[i][j])

np.savez('points', x=x, y=y, z=z)
np.savez_compressed('points_compressed', x=x, y=y, z=z)

print(f"Size of points.npz:            {os.path.getsize('points.npz')}")
print(f"Size of points_compressed.npz: {os.path.getsize('points_compressed.npz')}")