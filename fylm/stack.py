from fylm.model.roi import RegionOfInterest
from fylm.model.image import Image, LazyTif
from h5py import File as HDF5File
import numpy as np
from fylm import alignment
from fylm.model.constants import RotationDirection
from tifffile import TiffFile
from typing import Iterable


def create_roi_transformer(roi: RegionOfInterest):
    """
    Creates a function to normalize a given region of interest's raw image data.
    For example, we want all pombe catch tubes to be oriented with the drain to the left
    and the entrance to the right, but in the raw data, all tubes on the right side of the
    central trench have the drain on the right and entrance on the left.

    """
    if roi.flip_lr:
        return np.fliplr
    elif roi.rotate == RotationDirection.clockwise:
        return lambda image: alignment.cw_rotate(image)
    elif roi.rotate == RotationDirection.counterclockwise:
        return lambda image: alignment.ccw_rotate(image)
    else:
        return lambda image: image


class TiffReader(TiffFile):
    def __init__(self, filename: str):
        super().__init__(filename)
        self._index_map = self.micromanager_metadata['index_map']
        self._channel_names = self.micromanager_metadata['summary']['ChNames']

    def __iter__(self) -> Iterable[LazyTif]:
        for n, tif in enumerate(super().__iter__()):
            yield self[n]

    def __getitem__(self, index: int) -> LazyTif:
        fov = int(self._index_map['position'][index])
        frame = int(self._index_map['frame'][index])
        channel = self._channel_names[self._index_map['channel'][index]]
        z_level = int(self._index_map['slice'][index])
        return LazyTif(super().__getitem__(index), frame, 0.0, fov, channel, z_level)


class ImageStack(HDF5File):
    """
    Provides access to raw image data in an HDF5 file.

    """
    @property
    def fovs(self):
        yield from self.keys()

    def get_image(self, field_of_view: int, channel: str, z_offset: int, index):
        return self._get_data(field_of_view, channel, z_offset, index).value

    def get_attrs(self, field_of_view: int, channel: str, z_offset: int, index):
        return self._get_data(field_of_view, channel, z_offset, index).attrs

    def get_roi(self, roi: RegionOfInterest, channel: str, z_offset: int, index: int):
        """ Loads a single image from disk. """
        data = self._get_data(roi.field_of_view, channel, z_offset, index)
        image = data[roi.top_left.y: roi.bottom_right.y + 1,
                     roi.top_left.x: roi.bottom_right.y + 1]
        timestamp = data.attrs['timestamp']
        # TODO: WTF, no. Why tuple instead of object?
        return image, timestamp

    def _get_data(self, field_of_view: int, channel: str, z_offset: int, index):
        index = '/%d/%s/%d/%d' % (field_of_view, channel, z_offset, index)
        data = self.get(index)
        if data is None:
            raise ImageDoesNotExist(index)
        return data

    def indices(self, field_of_view: int, channel: str, z_offset: int):
        index = '/%d/%s/%d' % (field_of_view, channel, z_offset)
        data = self.get(index)
        return () if data is None else data.keys()


class ImageDoesNotExist(Exception):
    """
    You tried to get an image that doesn't exist.

    """
    def __init__(self, index):
        super().__init__()
        self.message = index


class ROIStack(object):
    """
    Provides access to the image stack for a single region of interest, and automatically applies transformations.

    """
    def __init__(self, image_stack: ImageStack, roi: RegionOfInterest):
        self._image_stack = image_stack
        self._roi = roi
        self._transformer = create_roi_transformer(roi)
        super().__init__()

    def get(self, channel: str, z_offset: int, index: int):
        image, timestamp = self._image_stack.get_roi(self._roi, channel, z_offset, index)
        return Image(self._transformer(image), index, timestamp, self._roi.field_of_view, channel, z_offset)
