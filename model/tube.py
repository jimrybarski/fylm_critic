from model.coordinates import Point, BoundingBox
from model.image import Image
import numpy as np


class CatchTube(BoundingBox):
    def __init__(self,
                 id_number: int,
                 field_of_view: int,
                 top_left: Point,
                 bottom_right: Point,
                 flip_lr=False,
                 rotate=False):
        super().__init__(top_left, bottom_right)
        assert not all((flip_lr, rotate))
        self._id = id_number
        self._field_of_view = field_of_view
        self._flip_lr = flip_lr
        self._rotate = rotate

    @property
    def id(self):
        return self._id

    @property
    def field_of_view(self):
        return self._field_of_view

    def extract(self, image: Image) -> np.ndarray:
        """
        We must always ensure that catch tubes are visualized with the drain to the left and the
        opening to the right, as that is how we will train image classifiers. Also, consistency is nice
        for comparison in figures.

        """
        assert image.field_of_view == self._field_of_view
        raw_data = image[self.top_left.y:self.bottom_right.y + 1,
                         self.top_left.x:self.bottom_right.x + 1]
        if self._flip_lr:
            raw_data = np.fliplr(raw_data)
        elif self._rotate:
            raise NotImplementedError("I don't know how to do this yet and need to look it up")
        return raw_data
