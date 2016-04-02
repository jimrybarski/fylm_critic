import unittest
from model.visualization import Movie
from model.coordinates import BoundingBox, Point
from model.tube import CatchTube
from model.image import Image
import numpy as np


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

    def test_offer(self):
        tube = CatchTube(0, 3, Point(0, 0), Point(20, 20))
        movie = Movie(tube).channel('BF')
        image = Image(np.array([[1, 0], [0, 1]]), 0, 0.0, 3, 'BF')
        self.assertIsNone(movie._images['BF'])
        self.assertEqual(movie._alphas['BF'], 1.0)
        movie.offer_image(image)
        self.assertTrue(np.array_equal(movie._images['BF'], image))
        self.assertEqual(movie._alphas['BF'], 1.0)

    def test_emit_not_ready(self):
        tube = CatchTube(0, 3, Point(0, 0), Point(20, 20))
        movie = Movie(tube).channel('BF')
        self.assertIsNone(movie.emit_frame())

    def test_emit_not_ready_fl_channels(self):
        tube = CatchTube(0, 3, Point(0, 0), Point(20, 20))
        movie = Movie(tube).channel('BF').channel('GFP')
        image = Image(np.array([[1, 0], [0, 1]]), 0, 0.0, 3, 'BF')
        movie.offer_image(image)
        self.assertIsNone(movie.emit_frame())

    def test_emit_two_channels(self):
        tube = CatchTube(0, 3, Point(0, 0), Point(20, 20))
        movie = Movie(tube).channel('BF').channel('GFP')
        bf_image = Image(np.array([[1, 0], [0, 1]]), 0, 0.0, 3, 'BF')
        gfp_image = Image(np.array([[1, 0], [0, 1]]), 0, 0.0, 3, 'GFP')
        movie.offer_image(bf_image)
        movie.offer_image(gfp_image)
        self.assertIsNotNone(movie.emit_frame())

    def test_fill_missing_fl_channels(self):
        tube = CatchTube(0, 3, Point(0, 0), Point(20, 20))
        movie = Movie(tube).channel('BF').channel('GFP').fill_missing_fluorescent_frames()
        bf_image = Image(np.array([[1, 0], [0, 1]]), 0, 0.0, 3, 'BF')
        bf_image2 = Image(np.array([[1, 0], [0, 1]]), 0, 0.0, 3, 'BF')
        gfp_image = Image(np.array([[1, 0], [0, 1]]), 0, 0.0, 3, 'GFP')

        movie.offer_image(bf_image)
        movie.offer_image(gfp_image)
        self.assertIsNotNone(movie.emit_frame())
        self.assertIsNone(movie.emit_frame())
        movie.offer_image(bf_image2)
        self.assertIsNotNone(movie.emit_frame())
