class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class BoundingBox(object):
    def __init__(self, top_left: Point, bottom_right: Point):
        self.top_left = top_left
        self.bottom_right = bottom_right
