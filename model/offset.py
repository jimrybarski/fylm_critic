from collections import defaultdict
from model.coordinates import Point
import statistics
from pandas import DataFrame


class RegistrationOffsets(object):
    """
    Stores translations needed to align images for each frame and field of view.

    """
    def __init__(self):
        self._offsets = defaultdict(dict)

    def __len__(self):
        return len(self._offsets)

    @property
    def df(self):
        data = [[field_of_view, frame_number, point.x, point.y] for field_of_view, data in self._offsets.items()
                for frame_number, point in data.items()]
        return DataFrame(data, columns=['field_of_view', 'frame_number', 'x', 'y'])

    def get(self, field_of_view: int, frame_number: int) -> Point:
        assert frame_number >= 0
        assert field_of_view >= 0
        return self._offsets[field_of_view][frame_number]

    def set(self, field_of_view: int, frame_number: int, offset: Point):
        assert frame_number >= 0
        assert offset is not None
        assert type(offset) == Point
        self._offsets[field_of_view][frame_number] = offset


class RotationOffsets(object):
    """
    Stores rotations needed to straighten images.

    """
    def __init__(self):
        self._offsets = {}

    def __len__(self):
        return len(self._offsets)

    @property
    def df(self):
        data = [[field_of_view, offset] for field_of_view, offset in self._offsets.items()]
        return DataFrame(data, columns=['field_of_view', 'offset'])

    def get(self, field_of_view: int):
        assert field_of_view >= 0
        offset = self._offsets.get(field_of_view)
        if offset is not None:
            return offset
        all_valid_offsets = [offset for offset in self._offsets.values() if offset is not None]
        return statistics.mean(all_valid_offsets)

    def set(self, field_of_view: int, offset: float):
        assert offset
        self._offsets[field_of_view] = offset
