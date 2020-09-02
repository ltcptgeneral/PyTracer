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

	def __init__(self, position, c):
		self.position = position
		self.color = c

class Scene():

	def __init__(self, camera, lights, objects, w, h, verbose = False):
		self.camera = camera
		self.lights = lights
		self.objects = objects
		self.w = w
		self.h = h
		self.verbose = verbose

	def render(self):
		aspect_ratio =  self.w / self.h
		x0 = -1.0
		x1 = +1.0
		x_delta = (x1 - x0) / (self.w - 1)

		y0 = -1.0 / aspect_ratio
		y1 = +1.0 / aspect_ratio
		y_delta = (y1 - y0) / (self.h - 1)

		pixels = Img(self.w, self.h)

		def ray_trace(ray):

			def find_nearest(ray):
				dist_min = None
				obj_hit = None

				for obj in self.objects:
					dist = obj.intersects(ray)
				if dist is not None and (obj_hit is None or dist < dist_min):
					dist_min = dist
					obj_hit = obj
				
				return (dist_min, obj_hit)

			def color_at(obj, pos, normal, specular_k = 50):
				m = obj.material
				obj_c = m.color_at(pos)
				camv = self.camera - pos
				c = m.ambient * Color.from_hex("#000000")

				for light in self.lights:
					lightv = Ray(pos, light.position - pos)
					c += obj_c * m.diffuse * max(normal * lightv.direction, 0) # Lambert
					hv = (lightv.direction + camv).unit()
					c += light.color * m.specular * max(normal * hv, 0) ** specular_k # Blinn-Phong

				return c

			c = Color(0, 0, 0)
			dist, obj = find_nearest(ray)
			if obj is None:
				return c
			pos = ray.origin + ray.direction * dist
			normal = obj.normal(pos)
			c += color_at(obj, pos, normal)
			return c

		for j in range(self.h):
			y = y1 - j * y_delta
			for i in range(self.w):
				x = x0 + i * x_delta
				r = Ray(self.camera, Point(x, y) - self.camera)
				pixels[j][i] = ray_trace(r)
			if self.verbose:
				print("{:3.0f}%".format(float(j)/float(self.h) * 100))

		return pixels

class Material():

	def __init__(self, c, ambient = 0.05, diffuse = 1.0, specular = 1.0):
		self.color = c
		self.ambient = ambient
		self.diffuse = diffuse
		self.specular = specular

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