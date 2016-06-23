import numpy as np
from collections import defaultdict
from typing import List


class LazyTif(object):
    """
    Holds metadata for a tif and a reference to the image data, but does not read the data from disk until requested.

    """
    def __init__(self, image_reference, frame: int, timestamp: float, field_of_view: int, channel: str, z_offset: int):
        assert frame >= 0
        assert timestamp >= 0.0
        assert field_of_view >= 0
        assert len(channel) > 0
        self._image_reference = image_reference
        self._frame = frame
        self._timestamp = timestamp
        self._field_of_view = field_of_view
        self._channel = channel
        self._z_offset = z_offset

    @property
    def as_image(self):
        return Image(self._image_reference.asarray(), self.frame, self.timestamp, self.field_of_view,
                     self.channel, self.z_offset)

    @property
    def index(self) -> str:
        return '%d/%d/%s/%d' % (self.field_of_view, self.frame, self.channel, self.z_offset)

    @property
    def frame(self) -> int:
        return self._frame

    @property
    def timestamp(self) -> float:
        return self._timestamp

    @property
    def field_of_view(self) -> int:
        return self._field_of_view

    @property
    def channel(self) -> str:
        return self._channel

    @property
    def z_offset(self) -> int:
        return self._z_offset


class Image(np.ndarray):
    """
    Holds the raw pixel data of an image and provides access to some metadata.

    """
    @staticmethod
    def combine(array: np.ndarray, image: 'Image'):
        # takes the pixel data from one source and the metadata from another Image and
        # combines them to create a new Image
        return Image(array, image.frame, image.timestamp, image.field_of_view, image.channel, image.z_offset)

    @property
    def index(self) -> str:
        return '%d/%d/%s/%d' % (self.field_of_view, self.frame, self.channel, self.z_offset)

    @property
    def frame(self) -> int:
        return self._frame

    @property
    def timestamp(self) -> float:
        return self._timestamp

    @property
    def field_of_view(self) -> int:
        return self._field_of_view

    @property
    def channel(self) -> str:
        return self._channel

    @property
    def z_offset(self) -> int:
        return self._z_offset

    # end users will not need to know anything about the methods below

    def __new__(cls, array, frame: int, timestamp: float, field_of_view: int, channel: str, z_offset: int):
        return np.asarray(array).view(cls)

    def __init__(self, array, frame: int, timestamp: float, field_of_view: int, channel: str, z_offset: int):
        assert frame >= 0
        assert timestamp >= 0.0
        assert field_of_view >= 0
        assert len(channel) > 0
        self._frame = frame
        self._timestamp = timestamp
        self._field_of_view = field_of_view
        self._channel = channel
        self._z_offset = z_offset

    def __array_wrap__(self, obj, *_):
        if len(obj.shape) == 0:
            return obj[()]
        else:
            return obj

    def __hash__(self) -> int:
        return hash((self.frame, self.timestamp, self.field_of_view, self.channel))

    def __eq__(self, other) -> bool:
        return other.index == self.frame and other.timestamp == self.timestamp \
               and other.field_of_view == self.field_of_view and other.channel == self.channel \
               and other.z_offset == self.z_offset


class Frame(object):
    """
    A container for several images taken at the same place and time.

    """
    def __init__(self, images: List[Image]):
        assert len(set(image.frame for image in images)) == 1, 'Frame was given images from separate time indexes'
        assert len(set(image.field_of_view for image in images)) == 1, 'Frame was given images from separate fields of view'
        self._images = defaultdict(dict)
        for image in images:
            self._images[image.channel][image.z_offset] = image

    def get(self, channel: str, z_offset: int=0) -> Image:
        """
        Attempts to return an Image matching the given criteria.

        Parameters
        ----------
        channel: the filter channel used to acquire the image (or "brightfield")
        z_offset: the distance in microns from the in-focus level

        """
        return self._images.get(channel).get(z_offset)
