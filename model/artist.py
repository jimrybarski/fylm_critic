from abc import abstractmethod
from model.color import Color
from model.coordinates import Point
from PIL import ImageDraw


class Artist(object):
    """
    Draws symbols and text on images. Typically this is for things like arrows that show locations of interesting
    features or bounding boxes, or even text. Classes should inherit from this and specify exactly how to draw their
    thing.

    """
    def __init__(self, coordinates: Point, color: Color):
        """
        :param coordinates:  the location of the pixel of interest. This is not necessarily the top-left corner of
        the Artist!

        """
        assert coordinates.x > 0 and coordinates.y > 0
        self._coordinates = coordinates
        self._color = color.hex

    @abstractmethod
    def draw(self, image_draw: ImageDraw):
        """
        Put the Artist's output onto the ImageDraw object.

        """
        raise NotImplementedError


class XCrossArtist(Artist):
    """
    Draws an X centered on the given coordinates.

    """
    def __init__(self, coordinates: Point, color: Color=Color(131, 245, 44), diameter: int=6, linewidth: int=3):
        super().__init__(coordinates, color)
        self._diameter = diameter
        self._linewidth = linewidth
        
    def draw(self, image_draw: ImageDraw):
        image_draw.line((self._coordinates.x - self._diameter, self._coordinates.y - self._diameter,
                         self._coordinates.x + self._diameter, self._coordinates.y + self._diameter),
                        fill=self._color, width=self._linewidth)
        image_draw.line((self._coordinates.x + self._diameter, self._coordinates.y - self._diameter,
                         self._coordinates.x - self._diameter, self._coordinates.y + self._diameter),
                        fill=self._color, width=self._linewidth)
