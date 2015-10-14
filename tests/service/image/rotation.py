import unittest
import numpy as np
from service.image.rotation import RotationCorrector
from model.image.rotation import RotationOffsets


class MockImage(np.ndarray):
    def __new__(cls, array):
        return np.asarray(array).view(cls)

    def __init__(self, array):
        self.frame_number = 5


class RotationTests(unittest.TestCase):
    def test_rotate(self):
        # just ensures that we're really rotating counterclockwise and that types are correct and such
        image = np.zeros((3, 3), dtype=np.bool)
        image[0][1] = 1
        image = MockImage(image)
        offsets = RotationOffsets()
        offsets[0] = 90.0
        rotated = RotationCorrector(offsets).adjust(image).astype(np.bool)
        expected = np.zeros((3, 3), dtype=np.bool)
        expected[1][0] = 1
        # test if the arrays are equal
        self.assertFalse((rotated - expected).any())
