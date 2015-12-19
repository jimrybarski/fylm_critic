import unittest
from model.artist import Artist
from model.coordinates import Point


class ArtistTests(unittest.TestCase):
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
