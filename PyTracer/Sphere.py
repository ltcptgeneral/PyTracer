from math import sqrt

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