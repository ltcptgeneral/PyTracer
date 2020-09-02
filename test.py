from PyTracer import color
from PyTracer import camera
from PyTracer import point
from PyTracer import sphere
from PyTracer import scene

import time

WIDTH = 320
HEIGHT = 200

c = point(0, 0, -1)
objects = [sphere(point(0, 1, 0), 0.5, color.from_hex("#FF0000"))]
s = scene(c, objects, WIDTH, HEIGHT)
start = time.time()
i = s.render()
end = time.time()

print("render completed in {} seconds".format(end-start))

with open ("test.ppm", "w") as f:
    i.PPM(f)