'''
Referencias:
- http://www.cs.cornell.edu/courses/cs4620/2013fa/lectures/03raytracing1.pdf
- https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-box-intersection
'''

from lib import *
from plane import Plane

class Cube(object):
    def __init__(self, position, size, material):
        self.material = material
        self.position = position
        self.min_boundaries = []
        self.max_boundaries = []
        self.planes = []
        self.half_size = size / 2
        self.generate_boundaries()
        self.generate_planes()
    
    def generate_planes(self):
        planesPositionMatrix = [
                [self.half_size, 0, 0],
                [-self.half_size, 0, 0],
                [0, self.half_size, 0],
                [0, -self.half_size, 0],
                [0, 0, self.half_size],
                [0, 0, -self.half_size]
            ]
        
        FacesDirectionMatrix = [
                [1, 0, 0],
                [-1, 0, 0],
                [0, 1, 0],
                [0, -1, 0],
                [0, 0, 1],
                [0, 0, -1]
            ]
        
        for plane_position, face_direction in zip(planesPositionMatrix, FacesDirectionMatrix):            
            self.planes.append(Plane(sum(self.position, V3(plane_position[0], plane_position[1], plane_position[2])),
                                     V3(face_direction[0], face_direction[1], face_direction[2]),
                                     self.material))
    
    def generate_boundaries(self):
        epsilon = 0.001
        for i in range(3):
            self.min_boundaries.append(self.position[i] - (epsilon + self.half_size))
            self.max_boundaries.append(self.position[i] + (epsilon + self.half_size))

    def ray_intersect(self, orig, direction):
        t = float('inf')
        intersect = None

        for plane in self.planes:
            intersection = plane.ray_intersect(orig, direction)

            if intersection is not None:
                if self.min_boundaries[0] <= intersection.point[0] <= self.max_boundaries[0]:
                    if self.min_boundaries[1] <= intersection.point[1] <= self.max_boundaries[1]:
                        if self.min_boundaries[2] <= intersection.point[2] <= self.max_boundaries[2]:
                            if intersection.distance < t:
                                t = intersection.distance
                                intersect = intersection

        if intersect is None:
            return None

        return Intersect(distance = intersect.distance,
                         point = intersect.point,
                         normal = intersect.normal)
