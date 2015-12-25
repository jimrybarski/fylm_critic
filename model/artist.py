from abc import abstractmethod
from model.coordinates import Point
from PIL import Image, ImageDraw
import numpy as np


class Artist(object):
    """
    Draws symbols and text on images. Typically this is for things like arrows that show locations of interesting
    features or bounding boxes, or even text. Classes should inherit from this and specify exactly how to draw their
    thing.

    """
    def __init__(self, coordinates: Point, color="#83F52C"):
        """
        :param coordinates:  the location of the pixel of interest. This is not necessarily the top-left corner of
        the artist!

        """
        assert coordinates.x > 0 and coordinates.y > 0
        self._coordinates = coordinates
        self._color = color

    @abstractmethod
    def _draw(self, image: Image):
        raise NotImplementedError

    def draw(self, image_draw: ImageDraw) -> np.ndarray:
        self._draw(image_draw)


class XCrossArtist(Artist):
    def __init__(self, coordinates: Point, diameter=6, linewidth=3, color="#83F52C"):
        super().__init__(coordinates, color)
        self._diameter = diameter
        self._linewidth = linewidth
        
    def _draw(self, canvas: ImageDraw):
        canvas.line((self._coordinates.x - self._diameter, self._coordinates.y - self._diameter,
                     self._coordinates.x + self._diameter, self._coordinates.y + self._diameter),
                    fill=self._color, width=self._linewidth)
        canvas.line((self._coordinates.x + self._diameter, self._coordinates.y - self._diameter,
                     self._coordinates.x - self._diameter, self._coordinates.y + self._diameter),
                    fill=self._color, width=self._linewidth)
