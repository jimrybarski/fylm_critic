import unittest
from model.image.offset import Offsets


class RotationOffsetsTests(unittest.TestCase):
    def setUp(self):
        self.offsets = Offsets()
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
        offsets = Offsets()
        offsets[0] = 10.0
        self.assertEqual(offsets[0], 10.0)
        self.assertEqual(offsets[100], 10.0)
        self.assertEqual(offsets[1000], 10.0)
        self.assertEqual(offsets[10000], 10.0)

    def test_length(self):
        self.assertEqual(len(self.offsets), 1010)
