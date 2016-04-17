from fylm.model.roi import PombeCatchTube
from fylm.model.coordinates import Point
import unittest
import numpy as np
from fylm.model.image import Image


class TubeTests(unittest.TestCase):
    def test_one_rotation_limit(self):
        with self.assertRaises(AssertionError):
            tube = PombeCatchTube(1, 3, Point(20, 20), Point(30, 30), flip_lr=True, rotate=90)
        tube = PombeCatchTube(1, 3, Point(20, 20), Point(30, 30), flip_lr=True)
        self.assertTrue(tube._flip_lr)
        self.assertFalse(tube._rotate)
        tube = PombeCatchTube(1, 3, Point(20, 20), Point(30, 30), rotate=90)
        self.assertFalse(tube._flip_lr)
        self.assertTrue(tube._rotate)

    def test_extract_normal(self):
        raw_image = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0],
                              [0, 0, 2, 4, 4, 4, 2, 0, 0, 0, 0, 0],
                              [0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        image = Image(raw_image, 0, 0.0, 3, 'BF', 0)
        tube = PombeCatchTube(0, 3, Point(2, 1), Point(6, 3))
        expected = np.array([[0, 2, 2, 2, 0],
                             [2, 4, 4, 4, 2],
                             [0, 2, 2, 2, 0]])
        # self.assertTrue(np.array_equal(extracted_image, expected))
        # self.assertEqual(extracted_image.shape, expected.shape)

    def test_extract_fliplr(self):
        raw_image = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 7, 2, 2, 0, 0, 0, 0, 0, 0],
                              [0, 0, 9, 4, 4, 4, 2, 0, 0, 0, 0, 0],
                              [0, 0, 0, 9, 2, 2, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        image = Image(raw_image, 0, 0.0, 3, 'BF', 0)
        tube = PombeCatchTube(0, 3, Point(2, 1), Point(6, 3), flip_lr=True)
        expected = np.array([[0, 2, 2, 7, 0],
                             [2, 4, 4, 4, 9],
                             [0, 2, 2, 9, 0]])
        # self.assertTrue(np.array_equal(extracted_image, expected))
        # self.assertEqual(extracted_image.shape, expected.shape)

    def test_rotate(self):
        raw_image = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 3, 4, 2, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 3, 4, 2, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 3, 4, 2, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        image = Image(raw_image, 0, 0.0, 3, 'BF', 0)
        tube = PombeCatchTube(0, 3, Point(3, 1), Point(5, 5), rotate=90)
        expected = np.array([[0, 3, 3, 3, 0],
                             [2, 4, 4, 4, 9],
                             [0, 2, 2, 2, 0]])
        # self.assertTrue(np.array_equal(extracted_image, expected))
        # self.assertEqual(extracted_image.shape, expected.shape)
