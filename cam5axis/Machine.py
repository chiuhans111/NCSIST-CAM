import numpy as np
from cam5axis.utils import *


class Knife:
    def __init__(self, vec, pos):
        self.vec = norm(np.array(vec))
        self.pos = np.array(pos)


class Axis:
    def __init__(self, vec, min, max):
        self.vec = norm(np.array(vec))
        self.min = min
        self.max = max

    def check(self, val):
        return min <= val <= max


class RotationAxis(Axis):
    def __init__(self, vec, pos, min, max):
        super(RotationAxis, self).__init__(vec, min, max)
        self.pos = np.array(pos)



class Machine:
    def __init__(self):
        self.x = Axis([1, 0, 0], -100, 100)
        self.y = Axis([0, 1, 0], -100, 100)
        self.z = Axis([0, 0, 1], -100, 100)

        self.a = RotationAxis([0, 0, 1], [0, 1, -1], np.pi, -np.pi)
        self.b = RotationAxis([1, 0, 0], [1, 0, -2], np.pi, 0)

        self.n = Knife([0, 0, 1], [0, -1, -3])

        self.origin = np.array([0, 0, 0])
