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