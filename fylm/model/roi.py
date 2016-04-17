from fylm.model.coordinates import Point
from typing import Union


class RegionOfInterest(object):
    def __init__(self, id_number: int, field_of_view: int, top_left: Point, bottom_right: Point,
                 flip_lr: bool=False, rotate: Union[bool, str]=False):
        assert top_left.x < bottom_right.x
        assert top_left.y < bottom_right.y
        assert not all((flip_lr, rotate))
        assert rotate in (False, 'clockwise', 'counterclockwise')

        self._id = id_number
        self._top_left = top_left
        self._bottom_right = bottom_right
        self._field_of_view = field_of_view
        self._flip_lr = flip_lr
        self._rotate = rotate

    @property
    def id(self) -> int:
        return self._id

    @property
    def top_left(self) -> Point:
        return self._top_left

    @property
    def bottom_right(self) -> Point:
        return self._bottom_right

    @property
    def field_of_view(self) -> int:
        return self._field_of_view

    @property
    def flip_lr(self) -> bool:
        return self._flip_lr

    @property
    def rotate(self) -> Union[bool, str]:
        return self._rotate
