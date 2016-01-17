from model.artist import Artist
import numpy as np
from PIL import Image, ImageDraw
from model import color


class Canvas(object):
    def __init__(self, image: np.array):
        self._background_image = color.convert_to_rgb(image)
        self._artists = []

    def add_overlay(self, image: np.array, display_color: color.Color, alpha: float=1.0):
        """
        Put another image on top of the background greyscale one. Usually, this is for adding
        fluorescent data on top of a bright field image.

        """
        assert len(image.shape) == 2, 'image must be greyscale'
        self._background_image += (display_color * image * alpha).astype('uint8')

    def add_artist(self, artist: Artist):
        """
        Add an artist that will draw something onto the images.

        """
        self._artists.append(artist)

    @property
    def image(self) -> np.array:
        """
        Puts all the images and artists together to create a single image.

        """
        pil_image = Image.fromarray(self._background_image, "RGB")
        image_draw = ImageDraw.Draw(pil_image)
        for artist in self._artists:
            artist.draw(image_draw)
        return np.array(pil_image)
