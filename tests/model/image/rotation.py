import unittest
from model.image.rotation import RotationOffsets


class RotationOffsetsTests(unittest.TestCase):
    def setUp(self):
        self.offsets = RotationOffsets()
        self.offsets._values = {0: 12.3, 560: 11.7, 1010: 1.3}

    def test_getitem_exact(self):
        self.assertEqual(self.offsets[0], 12.3)

    def test_getitem_middle(self):
        self.assertEqual(self.offsets[250], 12.3)

    def test_getitem_exact_2nd(self):
        self.assertEqual(self.offsets[560], 11.7)

    def test_getitem_middle_2nd(self):
        self.assertEqual(self.offsets[900], 11.7)

    def test_setitem(self):
        offsets = RotationOffsets()
        offsets[0] = 10.0
        self.assertEqual(offsets[0], 10.0)
        self.assertEqual(offsets[100], 10.0)
        self.assertEqual(offsets[1000], 10.0)
        self.assertEqual(offsets[10000], 10.0)

    def test_last_real_value(self):
        self.assertEqual(self.offsets.last_real_value, 1010)
