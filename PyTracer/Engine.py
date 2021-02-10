from multiprocessing import Pool
from itertools import repeat
import os

from .Img import Img
from .Ray import Ray
from .Point import Point
from .Color import Color

class Engine():

	def __init__(self, max_depth = 5, min_displacement = 0.0001):
		self.MAX_DEPTH = max_depth
		self.MIN_DISPLACE = min_displacement
	
	def find_nearest(self, ray, scene):
		dist_min = None
		obj_hit = None
		for obj in scene.objects:
			dist = obj.intersects(ray)
			if dist is not None and (obj_hit is None or dist < dist_min):
				dist_min = dist
				obj_hit = obj
		return (dist_min, obj_hit)

	def color_at(self, obj_hit, hit_pos, normal, scene):
		material = obj_hit.material
		obj_color = material.color_at(hit_pos)
		to_cam = scene.camera - hit_pos
		specular_k = 50
		color = material.ambient * Color.from_hex("#FFFFFF")
		for light in scene.lights:
			to_light = Ray(hit_pos, light.position - hit_pos)
			color += (
				obj_color
				* material.diffuse
				* max(normal * to_light.direction, 0)
			)
			half_vector = (to_light.direction + to_cam).unit()
			color += (
				light.color
				* material.specular
				* max(normal * half_vector, 0) ** specular_k
			)
		return color

	def ray_trace(self, data, depth = 0):
		ray = data[0]
		scene = data[1]
		color = Color(0, 0, 0)
		dist_hit, obj_hit = self.find_nearest(ray, scene)
		if obj_hit is None:
			return color
		hit_pos = ray.origin + ray.direction * dist_hit
		hit_normal = obj_hit.normal(hit_pos)
		color += self.color_at(obj_hit, hit_pos, hit_normal, scene)

		if depth < self.MAX_DEPTH:
			new_ray_pos = hit_pos + hit_normal * self.MIN_DISPLACE
			new_ray_dir = (
				ray.direction - 2 * (ray.direction * hit_normal) * hit_normal
			)
			new_ray = Ray(new_ray_pos, new_ray_dir)
			color += (
				self.ray_trace((new_ray, scene), depth + 1) * obj_hit.material.reflection
			)

		return color

	def render(self, scene, threads = os.cpu_count()):
		width = scene.width
		height = scene.height
		aspect_ratio = float(width) / height
		x0 = -1.0
		x1 = +1.0
		xstep = (x1 - x0) / (width - 1)
		y0 = -1.0 / aspect_ratio
		y1 = +1.0 / aspect_ratio
		ystep = (y1 - y0) / (height - 1)

		camera = scene.camera
		pixels = Img(width, height)

		raw_rays = []

		for j in range(height):
			y = y1 - (j * ystep)
			for i in range(width):
				x = x0 + i * xstep
				ray = Ray(camera, Point(x, y) - camera)
				raw_rays.append((ray, scene))

		p = Pool(processes = threads)

		traced = p.map(self.ray_trace, raw_rays)

		index = 0

		for j in range(height):
			y = y1 - (j * ystep)
			for i in range(width):
				x = x0 + i * xstep
				pixels[j][i] = traced[index]
				index+=1

		return pixels