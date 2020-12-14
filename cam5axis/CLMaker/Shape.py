import numpy as np


class Shape:
    def get_bounding_box(self):
        # left bottom, right top
        return np.array([[-1, -1], [1, 1]])

    def get_edge_distant(self, vec):
        # negative inside
        return np.sqrt(np.sum(vec**2)) - 1

    def ray_marching(self, pos, vec, iteration=10, far=1e10, factor=.99):
        l = 0
        vec = np.array(vec)
        vec /= np.sqrt(np.sum(vec**2))
        for i in range(iteration):
            p = pos + vec * l
            l += self.get_edge_distant(p) * factor
            if l > far:
                return False
        return pos + vec * l


class CircleShape(Shape):
    def __init__(self, center, radius):
        self.center = np.array(center)
        self.radius = radius

    def get_bounding_box(self):
        return np.array([self.center-radius, self.center+radius])

    def get_edge_distant(self, vec):
        return np.sqrt(np.sum((vec-self.center)**2)) - self.radius


class PolygonShape(Shape):
    def __init__(self, path):
        self.path = path

    def get_bounding_box(self):
        return np.array([np.min(self.path, axis=0), np.max(self.path, axis=0)])
    
    def get_edge_distant(self, vec):

