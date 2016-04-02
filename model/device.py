from model.coordinates import Point, BoundingBox


class Device(object):
    ORIGINAL_FYLM = 1
    NEW_FYLM = 2
    PLINKO = 3
    CEREVISIAE = 4


class CatchTube(BoundingBox):
    def __init__(self, top_left: Point, bottom_right: Point, field_of_view: int):
        super().__init__(top_left, bottom_right)
        self._field_of_view = field_of_view
