import numpy as np


class Image(np.ndarray):
    """
    Holds the raw pixel data of an image and provides access to some metadata.

    """
    def __new__(cls, array, index, timestamp, field_of_view, channel):
        return np.asarray(array).view(cls)

    def __init__(self, array, index, timestamp, field_of_view, channel):
        assert index >= 0
        assert timestamp >= 0.0
        assert field_of_view >= 0
        assert len(channel) > 0
        self._index = index
        self._timestamp = timestamp
        self._field_of_view = field_of_view
        self._channel = channel

    def __array_wrap__(self, obj, *_):
        if len(obj.shape) == 0:
            return obj[()]
        else:
            return obj

    @property
    def index(self):
        return self._index

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def field_of_view(self):
        return self._field_of_view

    @property
    def channel(self):
        return self._channel
