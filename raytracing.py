from lib import *
from math import pi, tan
from random import random
from cube import *
from triangle import *
from obj import *

BLACK = color(0, 0, 0)
SKY = color(134, 184, 235)

MAX_RECURSION_DEPTH = 3

class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background_color = SKY
        self.light = None
        self.clear()
    
    def clear(self):
        self.pixels = [
            [BLACK for _ in range(self.width)]
            for _ in range(self.height)
            ]
    
    def write(self, filename):
        writeBMP(filename, self.width, self.height, self.pixels)
    
    def point(self, x, y, col):
        self.pixels[y][x] = col
    
    def cast_ray(self, origin, direction, recursion = 0):
        material, intersect = self.scene_intersect(origin, direction)
        
        if material is None or recursion >= MAX_RECURSION_DEPTH:
            return self.background_color
        
        light_dir = norm(sub(self.light.position, intersect.point))
        
        offset_normal = mul(intersect.normal, 0.1)
        shadow_orig = sum(intersect.point, offset_normal) \
                       if dot(light_dir, intersect.normal) >= 0 \
                       else sub(intersect.point, offset_normal)
        
        shadow_material, shadow_intersect = self.scene_intersect(shadow_orig, light_dir)
        if shadow_material is None:
            shadow_intensity = 0
        else:
            shadow_intensity = 0.5
        
        if material.albedo[2] > 0:
            reverse_direction = mul(direction, -1)
            reflect_direction = reflect(reverse_direction, intersect.normal)
            reflect_orig = sum(intersect.point, offset_normal) \
                       if dot(reflect_direction, intersect.normal) >= 0 \
                       else sub(intersect.point, offset_normal)
            
            reflect_color = self.cast_ray(reflect_orig, reflect_direction, recursion + 1)
        else:
            reflect_color = color(0, 0, 0)
            
        if material.albedo[3] > 0:
            refract_direction = refract(direction, intersect.normal, material.refractive_index)
            if refract_direction is None:
                refract_color = color(0, 0, 0)
            else:            
                refract_orig = sum(intersect.point, offset_normal) \
                           if dot(reflect_direction, intersect.normal) >= 0 \
                           else sub(intersect.point, offset_normal)
                
                refract_color = self.cast_ray(refract_orig, refract_direction, recursion + 1)
        else:
            refract_color = color(0, 0, 0)
        
        diffuse_intensity = self.light.intensity * max(0, dot(light_dir, intersect.normal)) \
        * (1 - shadow_intensity)
        
        if shadow_intensity > 0:
            specular_intensity = 0
        else:            
            specular_reflection = reflect(light_dir, intersect.normal)
            specular_intensity = self.light.intensity * (
                    max(0, dot(specular_reflection, direction)) ** material.spec
                )
        
        diffuse = material.diffuse * diffuse_intensity * material.albedo[0]
        specular = self.light.color * specular_intensity * material.albedo[1]
        reflection =  reflect_color * material.albedo[2]
        
        refraction = refract_color * material.albedo[3]
        
        if material.texture and intersect.text_coords is not None:
            text_color = material.texture.get_color(intersect.text_coords[0], intersect.text_coords[1])
            diffuse = text_color * 255
        
        c = diffuse + specular + reflection + refraction
        
        return c
    
    def scene_intersect(self, origin, direction):
        zbuffer = float('inf')
        material = None
        intersect = None
        
        for obj in self.scene:
            r_intersect = obj.ray_intersect(origin, direction)
            
            if r_intersect and r_intersect.distance < zbuffer:
                zbuffer = r_intersect.distance
                material = obj.material
                intersect = r_intersect
            
        return material, intersect
    
    def render(self):
        fov = pi/2
        aspect_ratio = self.width/self.height
        
        for y in range(self.height):
            for x in range(self.width):
                if random() > 0:
                    i = (2 * ((x + 0.5)/self.width) - 1) * aspect_ratio * tan(fov/2)
                    j = 1 - 2 * ((y + 0.5)/self.height) * tan(fov/2)
                    
                    direction = norm(V3(i, j, -1))
                    col = self.cast_ray(V3(0, 0, 0), direction)
                    self.point(x, y, col)

    def Load(self, filename, translate, scale):
        model = Obj(filename)        
        triangles_vertex = []
        
        for face in model.faces:
            f1 = face[0][0] - 1
            f2 = face[1][0] - 1
            f3 = face[2][0] - 1
            
            A = Transform(model.vertices[f1], translate, scale)
            B = Transform(model.vertices[f2], translate, scale)
            C = Transform(model.vertices[f3], translate, scale)
            triangles_vertex.append([A, B, C])
            
        return triangles_vertex
