import unittest
from model.visualization import Movie
from model.coordinates import BoundingBox, Point


class MovieTest(unittest.TestCase):
    def test_full_chain(self):
        m = Movie(BoundingBox(Point(0, 0), Point(10, 10))).channel("BF").channel("GFP", alpha=0.5)
        m = m.fill_missing_fluorescent_frames().stop(12413512.1).start(0.0)
        self.assertTrue(isinstance(m, Movie))

    def test_start_stop_order(self):
        with self.assertRaises(AssertionError):
            Movie(BoundingBox(Point(0, 0), Point(10, 10))).start(45).stop(0)

        with self.assertRaises(AssertionError):
            Movie(BoundingBox(Point(0, 0), Point(10, 10))).stop(1).start(123)

        with self.assertRaises(AssertionError):
            Movie(BoundingBox(Point(0, 0), Point(10, 10))).stop(0)
