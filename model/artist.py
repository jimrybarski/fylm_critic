from model.coordinates import Point
import numpy as np


class OutOfBoundsError(Exception):
    """
    A requested Artist isn't in the image at all.

    """
    pass


class Artist(object):
    """
    Draws symbols and text on images. Typically this is for things like arrows that show locations of interesting features or bounding boxes, or even text.
    Classes should inherit from this and specify exactly how to draw their thing.

    """
    def __init__(self, coordinates: Point):
        """
        :param coordinates:  the location of the pixel of interest. This is not necessarily the top-left corner of the artist!

        """
        assert coordinates.x > 0 and coordinates.y > 0
        self._coordinates = coordinates

    # def draw_on(self, image: np.ndarray, image_top_left: Point, image_bottom_right: Point) -> np.ndarray:

    def _get_bounding_box(self) -> (Point, Point):
        """
        Provides global coordinates for the top left and bottom right corner of the bounding box of this Artist.

        """
        raise NotImplemented

    def _get_slice_coordinates(self, artist_top_left: Point, artist_bottom_right: Point, image_top_left: Point, image_bottom_right: Point) -> (int, int, int, int):
        # we assume Artists are significantly smaller than Images

        # If the artist's rendering cannot possibly have any overlap, we quit
        top_left_oob = artist_top_left.x > image_bottom_right.x or artist_top_left.y > image_bottom_right.y
        bottom_right_oob = artist_bottom_right.x < image_top_left.x or artist_bottom_right.y < image_top_left.y
        if top_left_oob or bottom_right_oob:
            raise OutOfBoundsError

        # now we find the array indices for the artist's image, to remove anything that's out of bounds
        top_left_x = max(0, image_top_left.x - artist_top_left.x)
        top_left_y = max(0, image_top_left.y - artist_top_left.y)

        artist_width = artist_bottom_right.x - artist_top_left.x + 1
        artist_height = artist_bottom_right.y - artist_top_left.y + 1
        bottom_right_x = min(artist_width, image_bottom_right.x - artist_bottom_right.x + 1)
        bottom_right_y = min(artist_height, image_bottom_right.y - artist_bottom_right.y + 1)
        return top_left_x, top_left_y, bottom_right_x, bottom_right_y
