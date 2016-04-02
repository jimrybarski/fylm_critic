import unittest
from model.visualization import Movie, FigureBuilder
from model.coordinates import Point
from model.tube import CatchTube
from model.image import Image
import numpy as np


class MovieTests(unittest.TestCase):
    def test_full_chain(self):
        m = Movie(CatchTube(0, 3, Point(0, 0), Point(10, 10))).add_channel("BF").add_channel("GFP", alpha=0.5)
        m = m.fill_missing_fluorescent_frames().set_stop(12413512.1).set_start(0.0)
        self.assertTrue(isinstance(m, Movie))

    def test_start_stop_order(self):
        with self.assertRaises(AssertionError):
            Movie(CatchTube(0, 3, Point(0, 0), Point(10, 10))).set_start(45).set_stop(0)

        with self.assertRaises(AssertionError):
            Movie(CatchTube(0, 3, Point(0, 0), Point(10, 10))).set_stop(1).set_start(123)

        with self.assertRaises(AssertionError):
            Movie(CatchTube(0, 3, Point(0, 0), Point(10, 10))).set_stop(0)


class FigureBuilderTests(unittest.TestCase):
    def test_offer(self):
        tube = CatchTube(0, 3, Point(0, 0), Point(20, 20))
        movie = Movie(tube).add_channel('BF')
        fb = FigureBuilder(movie)
        image = Image(np.array([[1, 0], [0, 1]]), 0, 0.0, 3, 'BF')
        self.assertIsNone(fb._images['BF'])
        fb.offer_image(image)
        self.assertTrue(np.array_equal(fb._images['BF'], image))

    def test_emit_not_ready(self):
        tube = CatchTube(0, 3, Point(0, 0), Point(20, 20))
        movie = Movie(tube).add_channel('BF')
        fb = FigureBuilder(movie)
        self.assertIsNone(fb.build())

    def test_emit_not_ready_fl_channels(self):
        tube = CatchTube(0, 3, Point(0, 0), Point(20, 20))
        movie = Movie(tube).add_channel('BF').add_channel('GFP')
        fb = FigureBuilder(movie)
        image = Image(np.array([[1, 0], [0, 1]]), 0, 0.0, 3, 'BF')
        fb.offer_image(image)
        self.assertIsNone(fb.build())

    def test_emit_two_channels(self):
        tube = CatchTube(0, 3, Point(0, 0), Point(20, 20))
        movie = Movie(tube).add_channel('BF').add_channel('GFP')
        fb = FigureBuilder(movie)
        bf_image = Image(np.array([[1, 0], [0, 1]]), 0, 0.0, 3, 'BF')
        gfp_image = Image(np.array([[1, 0], [0, 1]]), 0, 0.0, 3, 'GFP')
        fb.offer_image(bf_image)
        fb.offer_image(gfp_image)
        self.assertIsNotNone(fb.build())

    def test_fill_missing_fl_channels(self):
        tube = CatchTube(0, 3, Point(0, 0), Point(20, 20))
        movie = Movie(tube).add_channel('BF').add_channel('GFP').fill_missing_fluorescent_frames()
        fb = FigureBuilder(movie)
        bf_image = Image(np.array([[1, 0], [0, 1]]), 0, 0.0, 3, 'BF')
        bf_image2 = Image(np.array([[1, 2], [9, 4]]), 0, 0.0, 3, 'BF')
        gfp_image = Image(np.array([[2, 6], [3, 3]]), 0, 0.0, 3, 'GFP')

        fb.offer_image(bf_image)
        fb.offer_image(gfp_image)
        self.assertIsNotNone(fb.build())
        self.assertIsNone(fb.build())
        fb.offer_image(bf_image2)
        self.assertIsNotNone(fb.build())
