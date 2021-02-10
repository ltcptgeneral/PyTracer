from .Color import Color

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