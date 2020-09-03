from __future__ import division
import platform
from math import sqrt

class Vector:

	def __init__(self, x = 0.0, y = 0.0, z = 0.0):
		self.x = x
		self.y = y
		self.z = z

	def __str__(self):
		return "({}, {}, {})".format(self.x, self.y, self.z)

	def magnitude(self):
		return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

	def __abs__(self):
		return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

	def unit(self):
		return self / self.magnitude()

	def __add__(self, v):
		return Vector(self.x + v.x, self.y + v.y, self.z + v.z)
		
	def __sub__(self, v):
		return Vector(self.x - v.x, self.y - v.y, self.z - v.z)

	def __rsub__(self, v):
		return Vector(v.x - self.x, v.y - self.y, v.z - self.z)

	def __mul__(self, v):
		if type(v) == Vector:
			return (self.x * v.x + self.y * v.y + self.z * v.z)
		elif type(v) in [int, float]:
			return Vector(self.x * v, self.y * v, self.z * v)

	def __rmul__(self, v):
		if type(v) == Vector:
			return (self.x * v.x + self.y * v.y + self.z * v.z)
		elif type(v) in [int, float]:
			return Vector(self.x * v, self.y * v, self.z * v)

	def __truediv__(self, v):
		return Vector(self.x / v, self.y / v, self.z / v)

class Point(Vector):
	pass

class Ray():

	def __init__(self, origin, direction):
		self.origin = origin
		self.direction = direction.unit()

class Sphere():

	def __init__(self, center, radius, material):
		self.center = center
		self.radius = radius
		self.material = material

	def intersects(self, ray):
		sphere_to_ray = ray.origin - self.center
		# a = 1
		b = 2 * (ray.direction * sphere_to_ray)
		c = (sphere_to_ray * sphere_to_ray) - self.radius * self.radius
		discriminant = (b * b) - (4 * c)

		if discriminant >= 0:
			dist = (-b - sqrt(discriminant)) / 2
			if dist > 0:
				return dist
		return None

	def normal(self, position):
		return (position - self.center).unit()

class Camera():

	def __init__(self, position, direction):
		self.position = position
		self.direction = direction

class Light():

	def __init__(self, position, c = None):
		self.position = position
		if c is not None:
			self.color = c
		else:
			self.color = Color.from_hex("#FFFFFF")

class Scene():

	def __init__(self, camera, lights, objects, width, height):
		self.camera = camera
		self.objects = objects
		self.lights = lights
		self.width = width
		self.height = height

class Engine():

	def __init__(self, max_depth = 5, min_displacement = 0.0001):
		self.MAX_DEPTH = max_depth
		self.MIN_DISPLACE = min_displacement

	def render(self, scene):
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

		for j in range(height):
			y = y1 - (j * ystep)
			for i in range(width):
				x = x0 + i * xstep
				ray = Ray(camera, Point(x, y) - camera)
				pixels[j][i] = self.ray_trace(ray, scene)
			print("{:3.0f}%".format(float(j) / float(height) * 100), end="\r")
		return pixels

	def ray_trace(self, ray, scene, depth = 0):
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
				self.ray_trace(new_ray, scene, depth + 1) * obj_hit.material.reflection
			)

		return color

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

class Material():

	def __init__(self, c = None, ambient = 0.05, diffuse = 1.0, specular = 1.0, reflection = 0.5):
		if c is not None:
			self.color = c
		else:
			self.color = Color.from_hex("#FFFFFF")
		self.ambient = ambient
		self.diffuse = diffuse
		self.specular = specular
		self.reflection = reflection

	def color_at(self, position):
		return self.color

class Color(Vector):

	def __init__(self, r, g, b):
		self.x = r
		self.y = g
		self.z = b

	@classmethod
	def from_hex(cls, hexcolor = "#000000"):
		x = int(hexcolor[1:3], 16) / 255
		y = int(hexcolor[3:5], 16) / 255
		z = int(hexcolor[5:7], 16) / 255

		return cls(x, y, z)

	def __getattr__(self, name):
		if name == "r":
			return self.x
		elif name == "g":
			return self.y
		elif name == "b":
			return self.z
		else:
			raise AttributeError

class Img():

	def __init__(self, w, h):
		self.w = w
		self.h = h
		self.arr = [[Color(0, 0, 0) for _ in range(w)] for _ in range(h)]

	def PPM(self, imgfile, colorspace = 3, cmin = 0, cmax = 255):

		def to_byte(c):
			return round(max(min(c * cmax, cmax), cmin))

		imgfile.write("P3 {} {}\n{}\n".format(self.w, self.h, cmax))

		for row in self.arr:
			for pixel in row:
				imgfile.write("{} {} {} ".format(to_byte(pixel.x), to_byte(pixel.y), to_byte(pixel.z)))
			imgfile.write("\n")

	def __getitem__(self, index):	
		return self.arr[index]

	def __setitem__(self, index, value):
		self.arr[index] = value