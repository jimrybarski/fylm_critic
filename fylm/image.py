from fylm.model.roi import RegionOfInterest
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
