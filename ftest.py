from model.artist import XCrossArtist
from nd2reader import Nd2
from model.canvas import Canvas
import numpy as np
from model.coordinates import Point
from skimage import io

nd2 = Nd2("/var/nd2s/FYLM-141111-001.nd2")
background = nd2[2]
gfp = nd2[3] * (nd2[3] > np.mean(nd2[3]) + np.std(nd2[3]))
color = np.array([131, 245, 44]) / 255
artist = XCrossArtist(Point(100, 100))
artist2 = XCrossArtist(Point(500, 100))
artist3 = XCrossArtist(Point(500, 500))
artist4 = XCrossArtist(Point(300, 600))
canvas = Canvas(background)
canvas.add_overlay(gfp, color)

canvas.add_artist(artist)
canvas.add_artist(artist2)
canvas.add_artist(artist3)
canvas.add_artist(artist4)

io.imshow(canvas.combined_image)
io.show()
