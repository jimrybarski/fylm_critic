import unittest
from model.image.offset import RotationOffsets, RegistrationOffsets, Point


class RegistrationOffsetTests(unittest.TestCase):
    def setUp(self):
        self.offsets = RegistrationOffsets()

    def test_get(self):
        # Can we access translations?
        self.offsets._offsets[3][17] = Point(x=12.0, y=14.0)
        self.assertEqual(self.offsets.get(3, 17), Point(x=12.0, y=14.0))

    def test_set(self):
        # Can we store translations?
        self.offsets.set(3, 19, Point(13.0, 19.1))
        self.assertEqual(self.offsets._offsets[3][19], Point(13.0, 19.1))

    def test_length(self):
        # Can we tell how many translations we have?
        self.offsets.set(3, 19, Point(13.0, 19.1))
        self.offsets.set(3, 20, Point(14.0, 19.1))
        self.offsets.set(1, 0, Point(15.0, 19.1))
        self.assertEqual(len(self.offsets), 3)


class RotationOffsetsTests(unittest.TestCase):
    def setUp(self):
        self.offsets = RotationOffsets()
        self.offsets._offsets = {0: 11.7, 1: 178.0, 3: 11.3}

    def test_get(self):
        # Can we just get an offset?
        self.assertEqual(self.offsets.get(0), 11.7)

    def test_get_3(self):
        # Can we get different offsets?
        self.assertEqual(self.offsets.get(3), 11.3)

    def test_get_missing(self):
        # If we ask for an offset that couldn't be computed, will we get the average?
        self.assertEqual(self.offsets.get(7), 67.0)

    def test_setitem(self):
        # Can we store offsets?
        offsets = RotationOffsets()
        offsets.set(0, 10.0)
        self.assertEqual(offsets.get(0), 10.0)

    def test_length(self):
        # Can we tell how many offsets we have?
        self.assertEqual(len(self.offsets), 3)
