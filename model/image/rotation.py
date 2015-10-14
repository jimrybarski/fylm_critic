class RotationOffsets(object):
    """
    Stores offsets in degrees for each frame of an image stack.

    """
    def __init__(self):
        self._values = {}

    def __getitem__(self, frame_number: int) -> float:
        """
        Find the offset value or pick the offset from the closest frame with a value that preceded it.

        """
        assert frame_number >= 0
        offset = self._values.get(frame_number)
        if offset is not None:
            return offset
        closest_frame_number = max([n for n in self._values.keys() if n < frame_number])
        return self._values[closest_frame_number]

    def __setitem__(self, frame_number: int, offset: float):
        assert frame_number >= 0
        assert offset is not None
        self._values[frame_number] = offset

    @property
    def last_real_value(self) -> int:
        """
        Finds the highest frame number for which we have a record. We use this to prevent redoing work.

        """
        assert len(self._values) > 0
        return max(self._values.keys())
