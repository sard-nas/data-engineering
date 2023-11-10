import numpy as np
import json

matrix = np.load('matrix_74.npy')

data = {
    'sum': np.sum(matrix),
    'average': np.average(matrix),
    'sumMD': 0,
    'avgMD': 0,
    'sumSD': 0,
    'avgSD': 0,
    'max': np.max(matrix),
    'min': np.min(matrix)
}

size = len(matrix)
for i in range(size):
    for j in range(size):
        if i == j:
            data['sumMD'] += matrix[i][j]
        if i + j == size:
            data['sumSD'] += matrix[i][j]
data['avgMD'] = data['sumMD']/size
data['avgSD'] = data['sumSD']/size

norm_matrix = matrix / data['sum']
np.save('norm_matrix.npy', norm_matrix)

for key in data:
    data[key] = int(data[key])

with open('matrix_info.json', 'w') as outfile:
    outfile.write(json.dumps(data))