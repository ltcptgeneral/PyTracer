class Scene():

	def __init__(self, camera, lights, objects, width, height):
		self.camera = camera
		self.objects = objects
		self.lights = lights
		self.width = width
		self.height = height