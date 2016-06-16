from fylm.model.roi import RegionOfInterest
from fylm.model.coordinates import Point
import unittest
from fylm.model.constants import RotationDirection


class TubeTests(unittest.TestCase):
    def test_one_rotation_limit(self):
        with self.assertRaises(AssertionError):
            tube = RegionOfInterest(1, 3, Point(20, 20), Point(30, 30),
                                    RotationDirection.clockwise, flip_lr=True)
        tube = RegionOfInterest(1, 3, Point(20, 20), Point(30, 30),
                                RotationDirection.no_rotation, flip_lr=True)
        self.assertTrue(tube._flip_lr)
        self.assertFalse(tube._rotate)
        tube = RegionOfInterest(1, 3, Point(20, 20), Point(30, 30), RotationDirection.clockwise)
        self.assertFalse(tube._flip_lr)
        self.assertTrue(tube._rotate)
