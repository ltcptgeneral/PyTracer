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