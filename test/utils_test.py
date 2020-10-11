from cam5axis.utils import *
import numpy as np
print(rotation_matrix([1, 0, 0], [0, 1, np.pi]))
print(norm(np.array([1, 0, 0])))
print(norm(np.array([[1, 0, 0], [1, 1, 0], [0, 0, 1]])))


print('angle')

print(angle(
    np.array([[1, 0, 0], [1, 0, 0]]),
    np.array([[0, 1, 0], [1, 1, 1]]),
    np.array([[0, 0, 1], [0, 1, 0]])
))
