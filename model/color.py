import numpy as np
from skimage import color, img_as_float


def convert_to_rgb(image: np.array) -> np.array:
        """
        Converts an array to an 8-bit RGB image. This method is lossy and should only be used for
        visualizations.

        Parameters
        ----------
        image: 16-bit greyscale image

        """
        if len(image.shape) == 3:
            # image is already RGB
            return image
        assert len(image.shape) == 2, 'image must be greyscale'
        color_image = color.gray2rgb(img_as_float(image))
        return (255 * color_image).astype('uint8')


class Color(object):
    """
    Represents 8-bit colors.

    """
    def __init__(self, red: int, green: int, blue: int):
        if 0 <= red < 256 and 0 <= green < 256 and 0 <= blue < 256:
            self._red = red
            self._blue = blue
            self._green = green
            self._array = np.array([self._red, self._green, self._blue]) / 255
        else:
            raise ValueError("Color values are 8-bit and must be between 0 and 256")

    def convert(self, image: np.array) -> np.array:
        """
        Used to convert images from greyscale to monochromatic.

        >>> greyscale_image = np.array([[12000, 4200, 1800], [9000, 1200, 4400]], dtype='uint8')
        >>> color = Color(255, 0, 3)
        >>> color_image = color.convert(greyscale_image)
        >>> color_image.astype('uint8')
        array([[[224,   0,   2],
                [104,   0,   1],
                [  8,   0,   0]],

               [[ 40,   0,   0],
                [176,   0,   2],
                [ 48,   0,   0]]], dtype=uint8)

        """
        if len(image.shape) == 2:
            image = convert_to_rgb(image)
        return (image * self._array).astype(np.uint8)

    @property
    def hex(self) -> str:
        """
        An HTML-style color hex value used by the PIL library.

        >>> Color(255, 0, 3).hex
        '#ff0003'

        """
        return "#%02x%02x%02x" % (self._red, self._green, self._blue)
