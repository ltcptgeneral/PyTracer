from .Color import Color
from .BMP import Bitmap 

class Img():

	def __init__(self, w, h):
		self.w = w
		self.h = h
		self.arr = [[Color(0, 0, 0) for _ in range(w)] for _ in range(h)]

	def PPM(self, PATH, colorspace = 3, cmin = 0, cmax = 255):

		imgfile = open(PATH, "w")

		def to_byte(c):
			return round(max(min(c * cmax, cmax), cmin))

		imgfile.write("P3 {} {}\n{}\n".format(self.w, self.h, cmax))

		for row in self.arr:
			for pixel in row:
				imgfile.write("{} {} {} ".format(to_byte(pixel.x), to_byte(pixel.y), to_byte(pixel.z)))
			imgfile.write("\n")

		imgfile.close()

	def BMP(self, PATH, colorspace = 3, cmin = 0, cmax = 255):

		def to_byte(c):
			return round(max(min(c * cmax, cmax), cmin))

		b = Bitmap(self.w, self.h)

		for i in range(self.h):
			for j in range (self.w):
				pixel = self.arr[i][j]
				b.setPixel(j, self.h - i - 1, (to_byte(pixel.x), to_byte(pixel.y), to_byte(pixel.z)))

		b.write(PATH)

	def __getitem__(self, index):	
		return self.arr[index]

	def __setitem__(self, index, value):
		self.arr[index] = value