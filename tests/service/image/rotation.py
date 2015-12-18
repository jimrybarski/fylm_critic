import unittest
import numpy as np
from service.image.rotation import RotationCorrector
from model.image.offset import RotationOffsets


class MockImage(np.ndarray):
    def __new__(cls, array, frame_number=5):
        return np.asarray(array).view(cls)

    def __init__(self, array, frame_number=5):
        self.frame_number = frame_number
        self.field_of_view = 0


class RotationTests(unittest.TestCase):
    def test_rotate(self):
        # just ensures that we're really rotating counterclockwise and that types are correct and such
        image = np.zeros((3, 3), dtype=np.bool)
        image[0][1] = 1
        image = MockImage(image)
        offsets = RotationOffsets()
        offsets.set(0, 90.0)
        rotated = RotationCorrector(offsets).adjust(image).astype(np.bool)
        expected = np.zeros((3, 3), dtype=np.bool)
        expected[1][0] = 1
        # test if the arrays are equal
        self.assertFalse((rotated - expected).any())
