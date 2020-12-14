import numpy as np


class Axis:
    """
    Provides basic axis object definition
    """

    def __init__(self, min, max):
        self.min = min
        self.max = max

    def check_range(self, value):
        return self.min <= value <= self.max

    def clamp(self, value):
        if value < self.min:
            value = self.min

        if value > self.max:
            value = self.max

        return value

    def transform_matrix(self, value):
        return self.get_transform_matrix(self.clamp(value))

    def get_transform_matrix(self, value):
        return np.identity(4)


class TranslateAxis(Axis):
    def __init__(self, min, max, offset):
        super().__init__(min, max)
        self.offset = np.array(offset, "float64")

    def get_transform_matrix(self, value):
        mat = np.identity(4)
        mat[:3, 3] = self.offset * value
        return mat


class RotationAxis(Axis):
    def __init__(self, min, max, normal, position):
        super().__init__(min, max)
        self.normal = np.array(normal, "float64")
        self.normal /= np.sqrt(np.sum(self.normal**2))
        self.position = np.array(position)
        self.offset_axis = TranslateAxis(0, 0, position)

    def check_range(self, value):
        while value < self.min:
            value += np.pi*2
        while value > self.max:
            value -= np.pi*2

        return self.min <= value <= self.max

    def clamp(self, value):
        while value < self.min:
            value += np.pi*2
        while value > self.max:
            value -= np.pi*2

        if value < self.min:
            value = self.min

        if value > self.max:
            value = self.max

        return value

    def get_transform_matrix(self, value):
        mat_pre = self.offset_axis.get_transform_matrix(-1)
        mat_post = self.offset_axis.get_transform_matrix(1)

        cos = np.cos(value)
        sin = np.sin(value)

        ncos = np.identity(3)
        nsin = np.array([
            [0, -self.normal[2], self.normal[1]],
            [self.normal[2], 0, -self.normal[0]],
            [-self.normal[1], self.normal[0], 0]
        ])
        n1_cos = self.normal[:, np.newaxis] * self.normal[np.newaxis, :]
        mat_rot = np.identity(4)
        mat_rot[:3, :3] = cos*ncos + sin*nsin + (1-cos)*n1_cos

        return np.linalg.multi_dot([mat_post, mat_rot, mat_pre])

