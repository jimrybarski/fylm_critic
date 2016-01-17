class Point(object):
    def __init__(self, x, y):
        assert isinstance(x, int)
        assert isinstance(y, int)
        self.x = x
        self.y = y


class BoundingBox(object):
    def __init__(self, top_left: Point, bottom_right: Point):
        self.top_left = top_left
        self.bottom_right = bottom_right
