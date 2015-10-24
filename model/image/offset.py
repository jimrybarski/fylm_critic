class Offsets(dict):
    """
    Stores translations or rotations needed to align images. Basically this is just a dict

    """
    def __getitem__(self, frame_number: int):
        """
        We crudely interpolate missing values with a step function. For registration, we should not actually have missing values.

        """
        assert frame_number >= 0
        assert frame_number >= min(self.keys())
        offset = dict.__getitem__(self, frame_number)
        if offset is not None:
            return offset
        closest_frame_number = max([n for n in self.keys() if n < frame_number])
        return dict.__getitem__(self, closest_frame_number)

    def __setitem__(self, frame_number: int, offset):
        """
        We just add some assertions for safety, the behavior is not changed.

        """
        assert frame_number >= 0
        assert offset is not None
        dict.__setitem__(self, frame_number, offset)
