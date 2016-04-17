from fylm.model.roi import RegionOfInterest
from fylm.model.coordinates import Point
import unittest
import numpy as np
from fylm.model.image import Image


class TubeTests(unittest.TestCase):
    def test_one_rotation_limit(self):
        with self.assertRaises(AssertionError):
            tube = RegionOfInterest(1, 3, Point(20, 20), Point(30, 30), flip_lr=True, rotate='clockwise')
        tube = RegionOfInterest(1, 3, Point(20, 20), Point(30, 30), flip_lr=True)
        self.assertTrue(tube._flip_lr)
        self.assertFalse(tube._rotate)
        tube = RegionOfInterest(1, 3, Point(20, 20), Point(30, 30), rotate='clockwise')
        self.assertFalse(tube._flip_lr)
        self.assertTrue(tube._rotate)
