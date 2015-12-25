import matplotlib
matplotlib.use('Qt5Agg')
from model.coordinates import Point
from model.artist import XCrossArtist
from skimage import io, color
from nd2reader import Nd2
from skimage import img_as_float
from PIL import Image, ImageDraw
import numpy as np

nd2 = Nd2("/var/nd2s/FYLM-141111-001.nd2")
background = nd2[0]


thing = (255 * color.gray2rgb(img_as_float(background))).astype('uint8')
im = Image.fromarray(thing, "RGB")
image_draw = ImageDraw.Draw(im)

artist = XCrossArtist(Point(x=100, y=100), diameter=20, linewidth=5)
artist.draw(image_draw)
image = np.array(im)
io.imshow(image)
io.show()
