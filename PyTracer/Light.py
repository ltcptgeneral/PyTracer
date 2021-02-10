class Light():

	def __init__(self, position, c = None):
		self.position = position
		if c is not None:
			self.color = c
		else:
			self.color = Color.from_hex("#FFFFFF")