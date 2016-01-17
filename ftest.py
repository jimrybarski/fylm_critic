from model.artist import XCrossArtist
from model.canvas import Canvas
from model.color import Color
from model.coordinates import Point
from nd2reader import Nd2
import numpy as np
from skimage import io

nd2 = Nd2("/var/nd2s/FYLM-141111-001.nd2")
background_image = nd2[2]
gfp_image = nd2[3]
green = Color(131, 245, 44)
red = Color(255, 0, 0)

artist = XCrossArtist(Point(100, 100), color=red)
artist2 = XCrossArtist(Point(500, 100), color=red)
artist3 = XCrossArtist(Point(500, 500))
artist4 = XCrossArtist(Point(300, 600))

canvas = Canvas(background_image)
canvas.add_overlay(gfp_image, green)
canvas.add_artist(artist)
canvas.add_artist(artist2)
canvas.add_artist(artist3)
canvas.add_artist(artist4)

io.imshow(canvas.combined_image)
io.show()
