from collections import defaultdict


class Offsets(object):
    """
    Stores translations or rotations needed to align images. Basically this is just a dict

    """
    def __init__(self):
        self._offsets = defaultdict(dict)

    def __len__(self):
        return sum([len(value) for fov in self._offsets.values() for value in fov])
    
    def get(self, field_of_view: int, frame_number: int):
        """
        We crudely interpolate missing values with a step function.
        For registration, we should not actually have missing values in practice, but rotation definitely will.

        """
        assert frame_number >= 0
        assert field_of_view >= 0
        offset = self._offsets[field_of_view][frame_number]
        if offset is not None:
            return offset
        closest_frame_number = max([n for n in self._offsets[field_of_view].keys() if n < frame_number])
        return self._offsets[field_of_view][closest_frame_number]

    def set(self, field_of_view: int, frame_number: int, offset):
        assert frame_number >= 0
        assert offset is not None
        assert type(offset) == tuple
        self._offsets[field_of_view][frame_number] = offset
