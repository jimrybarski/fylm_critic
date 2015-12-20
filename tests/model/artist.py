import unittest
from model.artist import Artist, OutOfBoundsError
from model.coordinates import Point


class ArtistTests(unittest.TestCase):
    """
    These tests all basically just look for off-by-one errors.

    """
    def test_get_slice_coordinates(self):
        artist_top_left = Point(10, 10)
        artist_bottom_right = Point(20, 20)
        image_top_left = Point(0, 0)
        image_bottom_right = Point(50, 50)
        top_left_x, top_left_y, bottom_right_x, bottom_right_y = Artist(Point(15, 15))._get_slice_coordinates(artist_top_left, artist_bottom_right, image_top_left, image_bottom_right)
        self.assertEqual(top_left_x, 0)
        self.assertEqual(top_left_y, 0)
        self.assertEqual(bottom_right_x, 11)
        self.assertEqual(bottom_right_y, 11)

    def test_get_slice_coordinates_no_overlap(self):
        artist_top_left = Point(10, 10)
        artist_bottom_right = Point(20, 20)
        image_top_left = Point(300, 300)
        image_bottom_right = Point(500, 500)
        with self.assertRaises(OutOfBoundsError):
            Artist(Point(15, 15))._get_slice_coordinates(artist_top_left, artist_bottom_right, image_top_left, image_bottom_right)

    def test_get_slice_coordinates_partial_overlap_top(self):
        artist_top_left = Point(x=10, y=0)
        artist_bottom_right = Point(x=20, y=20)
        image_top_left = Point(0, 15)
        image_bottom_right = Point(50, 50)
        top_left_x, top_left_y, bottom_right_x, bottom_right_y = Artist(Point(15, 15))._get_slice_coordinates(artist_top_left, artist_bottom_right, image_top_left, image_bottom_right)
        self.assertEqual(top_left_x, 0)
        self.assertEqual(top_left_y, 15)
        self.assertEqual(bottom_right_x, 11)
        self.assertEqual(bottom_right_y, 21)

    def test_get_slice_coordinates_partial_overlap_top_left_corner(self):
        artist_top_left = Point(x=0, y=0)
        artist_bottom_right = Point(x=3, y=3)
        image_top_left = Point(1, 1)
        image_bottom_right = Point(5, 5)
        top_left_x, top_left_y, bottom_right_x, bottom_right_y = Artist(Point(15, 15))._get_slice_coordinates(artist_top_left, artist_bottom_right, image_top_left, image_bottom_right)
        self.assertEqual(top_left_x, 1)
        self.assertEqual(top_left_y, 1)
        self.assertEqual(bottom_right_x, 4)
        self.assertEqual(bottom_right_y, 4)

    def test_get_slice_coordinates_partial_overlap_bottom_right_corner(self):
        artist_top_left = Point(x=3, y=3)
        artist_bottom_right = Point(x=7, y=7)
        image_top_left = Point(1, 1)
        image_bottom_right = Point(5, 5)
        top_left_x, top_left_y, bottom_right_x, bottom_right_y = Artist(Point(15, 15))._get_slice_coordinates(artist_top_left, artist_bottom_right, image_top_left, image_bottom_right)
        self.assertEqual(top_left_x, 0)
        self.assertEqual(top_left_y, 0)
        self.assertEqual(bottom_right_x, 3)
        self.assertEqual(bottom_right_y, 3)

    def test_get_slice_coordinates_partial_overlap_right_side(self):
        artist_top_left = Point(x=3, y=2)
        artist_bottom_right = Point(x=7, y=4)
        image_top_left = Point(1, 1)
        image_bottom_right = Point(5, 5)
        artist = Artist(Point(15, 15))
        top_left_x, top_left_y, bottom_right_x, bottom_right_y = artist._get_slice_coordinates(artist_top_left,
                                                                                               artist_bottom_right,
                                                                                               image_top_left,
                                                                                               image_bottom_right)
        self.assertEqual(top_left_x, 0)
        self.assertEqual(top_left_y, 0)
        self.assertEqual(bottom_right_x, 3)
        self.assertEqual(bottom_right_y, 3)
