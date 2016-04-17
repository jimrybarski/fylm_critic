from fylm.model.coordinates import Point
from typing import Union
import numpy as np
from skimage import transform


class RegionOfInterest(object):
    def __init__(self, id_number: int, field_of_view: int, top_left: Point, bottom_right: Point,
                 flip_lr: bool=False, rotate: Union[bool, int]=False):
        assert top_left.x < bottom_right.x
        assert top_left.y < bottom_right.y
        assert not all((flip_lr, rotate))

        self._id = id_number
        self._top_left = top_left
        self._bottom_right = bottom_right
        self._field_of_view = field_of_view
        self._flip_lr = flip_lr
        self._rotate = rotate

    @property
    def transform(self):
        func = lambda image: image
        if self._flip_lr:
            func = lambda image: np.fliplr(image)
        elif self._rotate:
            func = lambda image: transform.rotate(image, self._rotate)
        return func

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

# class PombeCatchTube(RegionOfInterest):
#     """
#     Defines the area in an image where a catch tube is located. The tube doesn't not necessarily have
#     to contain any cells.
#
#     """
#     pass
#
# class CerevisiaeTrap(RegionOfInterest):
#     """
#     Defines the area in an image where a yeast trap is located. The trap doesn't not necessarily have
#     to contain any cells.
#
#     """
#     pass

    # def extract(self, image: Image) -> np.ndarray:
    #     """
    #     We must always ensure that catch tubes are visualized with the drain to the left and the
    #     opening to the right, as that is how we will train image classifiers. Also, consistency is nice
    #     for comparison in figures.
    #
    #     """
    #     # TODO: This is in the wrong place
    #     assert image.field_of_view == self._field_of_view
    #     raw_data = image[self.top_left.y:self.bottom_right.y + 1,
    #                      self.top_left.x:self.bottom_right.x + 1]
    #     if self._flip_lr:
    #         raw_data = np.fliplr(raw_data)
    #     elif self._rotate:
    #         raise NotImplementedError("I don't know how to do this yet and need to look it up")
    #     return raw_data
