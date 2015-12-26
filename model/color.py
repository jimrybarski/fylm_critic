import numpy as np
from skimage import color, img_as_float


class Color(object):
    def __init__(self, red, green, blue):
        if 0 <= red < 256 and 0 <= green < 256 and 0 <= blue < 256:
            self._rgb = np.array([red, green, blue]) / 255
        else:
            raise ValueError("Color values are 8-bit and must be between 0 and 256")

    @staticmethod
    def convert_to_rgb(image: np.array) -> np.ndarray:
        """
        Converts a raw, 16-bit greyscale image to an 8-bit RGB image.

        """
        assert len(image.shape) == 2, 'image must be greyscale'
        return (255 * color.gray2rgb(img_as_float(image))).astype('uint8')

    def __mul__(self, other):
        if len(other.shape) == 2:
            other = self.convert_to_rgb(other)
        return other * self._rgb

    def __rmul__(self, other):
        raise ArithmeticError("Color must always be the left operand in multiplication")

