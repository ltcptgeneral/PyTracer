from .Vector import Vector

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