from fylm.model.roi import RegionOfInterest
from fylm.model.image import Image
from h5py import File as HDF5File
import numpy as np


def create_roi_transformer(roi: RegionOfInterest):
    """
    Creates a function to normalize a given region of interest's raw image data.
    For example, we want all pombe catch tubes to be oriented with the drain to the left
    and the entrance to the right, but in the raw data, all tubes on the right side of the
    central trench have the drain on the right and entrance on the left.

    """
    if roi.flip_lr:
        return np.fliplr
    elif roi.rotate == 'clockwise':
        return lambda image: np.flipud(image).T
    elif roi.rotate == 'counterclockwise':
        return lambda image: np.flipud(image.T)
    else:
        return lambda image: image


class ImageStack(object):
    """
    Provides access to raw image data in an HDF5 file.

    """
    def __init__(self, filename: str):
        self._filename = filename
        self._hdf5 = None

    def __enter__(self):
        self._hdf5 = HDF5File(self._filename, 'a')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._hdf5.close()

    def get(self, roi: RegionOfInterest, channel: str, z_offset: int, index: int):
        """ Loads a single image from disk. """
        data = self._hdf5['/%d/%s/%d' % (roi.field_of_view, channel, z_offset)]
        image = data[roi.top_left.y: roi.bottom_right.y + 1,
                     roi.top_left.x: roi.bottom_right.y + 1,
                     index]
        timestamp = data.attrs['timestamp'][index]
        return image, timestamp


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
        image, timestamp = self._image_stack.get(self._roi, channel, z_offset, index)
        return Image(self._transformer(image), index, timestamp, self._roi.field_of_view, channel, z_offset)
