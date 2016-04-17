from fylm.model.image import Image
import numpy as np
import unittest


class TestImage(unittest.TestCase):
    def setUp(self):
        self.image = Image(np.random.randint(0, 65536, (512, 512)).astype(np.uint16),
                           13, 23562136136.311241, 8, 'GFP', 0)
        self.zeros = Image(np.zeros((512, 512)).astype(np.uint16), 13, 23562136136.311241, 8, 'GFP', 0)

    def test_attributes(self):
        self.assertEqual(self.image.index, 13)
        self.assertEqual(self.image.timestamp, 23562136136.311241)
        self.assertEqual(self.image.field_of_view, 8)
        self.assertEqual(self.image.channel, 'GFP')

    def test_addition(self):
        other_image = np.zeros((512, 512))
        combo = self.image + other_image
        self.assertTrue(np.array_equal(combo, self.image))

    def test_in_place_multiplication(self):
        self.image *= 0
        self.assertTrue(np.array_equal(np.zeros((512, 512)), self.image))
        self.assertEqual(self.image.field_of_view, 8)

    def test_aggregate(self):
        self.assertEqual(np.sum(self.zeros), 0)

    def test_slice(self):
        self.zeros[:, 0] = 1
        self.assertEqual(np.sum(self.zeros), 512)
