import numpy as np
from Quadtree import Point

class circle:

    def __init__(self, radius, center):
        self.radius = radius
        self.center = center

    def generate_circle_points(self, center, radius, num_points=100):
        angles = np.linspace(0, 2 * np.pi, num_points)
        return [Point(center.x + radius * np.cos(theta), center.y + radius * np.sin(theta)) for theta in angles]

