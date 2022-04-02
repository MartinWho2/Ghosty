import numpy as np
import random
import time

matrix = []


for row in range(1000):
    tmp = []
    for column in range(1000):
        tmp.append(random.randint(0,13))
    matrix.append(tmp)
if tmp:
    matrix.append(tmp)

array = np.array(matrix)
matrix_np = np.asmatrix(array)

initialTime = time.time()

for row in matrix:
    for column in row:
        if column != 0:
            pass
print(time.time()-initialTime)
initialTime = time.time()
for row in array:
    for tile in row:
        if tile != 0:
            2*3
print(time.time()-initialTime)
