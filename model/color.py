import numpy as np
from skimage import color, img_as_float


def convert_to_rgb(image: np.array) -> np.array:
        """
        Converts a raw, 16-bit greyscale image to an 8-bit RGB image.

        """
        assert len(image.shape) == 2, 'image must be greyscale'
        return (255 * color.gray2rgb(img_as_float(image))).astype('uint8')


class Color(object):
    """
    Represents 8-bit colors.

    """
    def __init__(self, red: int, green: int, blue: int):
        if 0 <= red < 256 and 0 <= green < 256 and 0 <= blue < 256:
            self._red = red
            self._blue = blue
            self._green = green
            self._array = None
        else:
            raise ValueError("Color values are 8-bit and must be between 0 and 256")

    @property
    def array(self) -> np.array:
        """
        Create a Numpy array needed by __mul__()

        """
        if self._array is None:
            self._array = np.array([self._red, self._green, self._blue]) / 255
        return self._array

    def __mul__(self, other: np.array) -> np.array:
        """
        Used to convert images from greyscale to monochromatic.

        >>> greyscale_image = np.array([[12000, 4200, 1800], [9000, 1200, 4400]], dtype='uint8')
        >>> color = Color(255, 0, 3)
        >>> color_image = color * greyscale_image
        >>> color_image.astype('uint8')
        array([[[224,   0,   2],
                [104,   0,   1],
                [  8,   0,   0]],

               [[ 40,   0,   0],
                [176,   0,   2],
                [ 48,   0,   0]]], dtype=uint8)

        """
        if len(other.shape) == 2:
            other = convert_to_rgb(other)
        return other * self.array

    def __rmul__(self, other):
        """
        We implement this just to provide a helpful error message.

        """
        raise ArithmeticError("Color must always be the left operand in multiplication")

    @property
    def hex(self) -> str:
        """
        An HTML-style color hex value used by the PIL library.

        >>> Color(255, 0, 3).hex
        '#ff0003'

        """
        return "#%02x%02x%02x" % (self._red, self._green, self._blue)
