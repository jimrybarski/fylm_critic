from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])


class BoundingBox(object):
    def __init__(self, top_left: Point, bottom_right: Point):
        self.top_left = top_left
        self.bottom_right = bottom_right
