import unittest
from fylm.image import cw_rotate, ccw_rotate, crop
import numpy as np


class AlignmentTests(unittest.TestCase):
    def test_cw_rotate(self):
        input = np.array([[1, 2, 3],
                          [4, 5, 6],
                          [7, 8, 9]])
        expected = np.array([[7, 4, 1],
                             [8, 5, 2],
                             [9, 6, 3]])
        actual = cw_rotate(input)
        self.assertTrue(np.array_equal(expected, actual))

    def test_ccw_rotate(self):
        input = np.array([[1, 2, 3],
                          [4, 5, 6],
                          [7, 8, 9]])
        expected = np.array([[3, 6, 9],
                             [2, 5, 8],
                             [1, 4, 7]])
        actual = ccw_rotate(input)
        self.assertTrue(np.array_equal(expected, actual))

    def test_crop(self):
        input = np.zeros((100, 100))
        actual = crop(input, 0.08)
        # expect to lose 8 pixels on both sides, so 100-16=84 remain
        expected = np.zeros((100, 84))
        self.assertTrue(np.array_equal(expected, actual))
