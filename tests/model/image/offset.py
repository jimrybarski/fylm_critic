import unittest
from model.image.offset import RotationOffsets, RegistrationOffsets


class RotationOffsetsTests(unittest.TestCase):
    def setUp(self):
        self.offsets = RotationOffsets()
        self.offsets._offsets = {0: 11.7, 1: 178.0, 3: 11.3}

    def test_get(self):
        self.assertEqual(self.offsets.get(0), 11.7)

    def test_get_3(self):
        self.assertEqual(self.offsets.get(3), 11.3)

    def test_get_missing(self):
        self.assertEqual(self.offsets.get(7), 67.0)

    def test_setitem(self):
        offsets = RotationOffsets()
        offsets.set(0, 10.0)
        self.assertEqual(offsets.get(0), 10.0)

    def test_length(self):
        self.assertEqual(len(self.offsets), 3)
