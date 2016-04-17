from fylm.model.roi import RegionOfInterest
from fylm.model.coordinates import Point
from fylm.image import create_roi_transformer
import numpy as np
import unittest


class TestImage(unittest.TestCase):
    def test_no_transform(self):
        tube = RegionOfInterest(0, 3, Point(2, 1), Point(6, 3))
        transformer = create_roi_transformer(tube)
        raw_image = np.array([[0, 2, 2, 2, 0],
                              [2, 4, 4, 4, 2],
                              [0, 2, 2, 2, 0]])
        expected = np.array([[0, 2, 2, 2, 0],
                             [2, 4, 4, 4, 2],
                             [0, 2, 2, 2, 0]])
        transformed_image = transformer(raw_image)
        self.assertTrue(np.array_equal(transformed_image, expected))
        self.assertEqual(transformed_image.shape, expected.shape)

    def test_flip_lr(self):
        tube = RegionOfInterest(0, 3, Point(2, 1), Point(6, 3), flip_lr=True)
        transformer = create_roi_transformer(tube)
        raw_image = np.array([[0, 7, 7, 2, 0],
                              [9, 4, 4, 4, 2],
                              [0, 2, 2, 1, 3]])
        expected = np.array([[0, 2, 7, 7, 0],
                             [2, 4, 4, 4, 9],
                             [3, 1, 2, 2, 0]])
        transformed_image = transformer(raw_image)
        self.assertTrue(np.array_equal(transformed_image, expected))
        self.assertEqual(transformed_image.shape, expected.shape)

    def test_clockwise(self):
        tube = RegionOfInterest(0, 3, Point(2, 1), Point(6, 3), rotate='clockwise')
        transformer = create_roi_transformer(tube)
        raw_image = np.array([[0, 7, 7, 2, 0],
                              [9, 4, 4, 4, 2],
                              [0, 2, 2, 1, 3]])
        expected = np.array([[0, 9, 0],
                             [2, 4, 7],
                             [2, 4, 7],
                             [1, 4, 2],
                             [3, 2, 0]])
        transformed_image = transformer(raw_image)
        self.assertTrue(np.array_equal(transformed_image, expected))
        self.assertEqual(transformed_image.shape, expected.shape)

    def test_counterclockwise(self):
        tube = RegionOfInterest(0, 3, Point(2, 1), Point(6, 3), rotate='counterclockwise')
        transformer = create_roi_transformer(tube)
        raw_image = np.array([[0, 7, 7, 2, 0],
                              [9, 4, 4, 4, 2],
                              [0, 2, 2, 1, 3]])
        expected = np.array([[0, 2, 3],
                             [2, 4, 1],
                             [7, 4, 2],
                             [7, 4, 2],
                             [0, 9, 0]])
        transformed_image = transformer(raw_image)
        self.assertTrue(np.array_equal(transformed_image, expected))
        self.assertEqual(transformed_image.shape, expected.shape)
