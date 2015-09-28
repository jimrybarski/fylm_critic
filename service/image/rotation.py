import logging
import math
import numpy as np
from scipy import ndimage
from skimage.filters import rank, threshold_otsu, vsobel
from skimage.morphology import disk, remove_small_objects, skeletonize
from skimage import transform

FIFTEEN_DEGREES_IN_RADIANS = 0.262

log = logging.getLogger(__name__)


def get_rotator(device: int):
    # We will probably have different devices in the future
    devices = {1: V1Rotator}
    return devices[device]()


class Rotator(object):
    @staticmethod
    def rotate(image: np.array, degrees: float) -> np.array:
        return transform.rotate(image, degrees)


class V1Rotator(Rotator):
    """ Determines the rotational skew of an image of a Version 1 FYLM device (the one with 28 channels per field of view and a large central trench. """
    ACCEPTABLE_SKEW_THRESHOLD = 5.0

    @staticmethod
    def calculate_skew(image: np.array) -> float:
        """ Finds rotational skew so that the sides of the central trench are (nearly) perfectly vertical. """
        vertical_edges = vsobel(image)
        # Convert the greyscale edge information into black and white (ie binary) image
        threshold = threshold_otsu(vertical_edges)
        # Filter out the edge data below the threshold, effectively removing some noise
        raw_channel_areas = vertical_edges <= threshold
        # Smooth out the data
        channel_areas = rank.mean(raw_channel_areas, disk(9)) < 200
        # Remove specks and blobs that are the result of artifacts
        clean_channel_areas = remove_small_objects(channel_areas, min_size=500)
        # Fill in any areas that are completely surrounded by the areas (hopefully) covering the channels
        segmentation = ndimage.binary_fill_holes(clean_channel_areas)
        # Draw a line that follows the center of the segments at each point, which should be roughly vertical
        # We should expect this to give us four approximately-vertical lines, possibly with many gaps in each line
        skeletons = skeletonize(segmentation)
        # Use the Hough transform to get the closest lines that approximate those four lines
        hough = transform.hough_line(skeletons, np.arange(-FIFTEEN_DEGREES_IN_RADIANS,
                                                          FIFTEEN_DEGREES_IN_RADIANS,
                                                          0.0001))
        # Create a list of the angles (in radians) of all of the lines the Hough transform produced, with 0.0 being
        # completely vertical
        # These angles correspond to the angles of the four sides of the channels, which we need to correct for
        angles = [angle for _, angle, dist in zip(*transform.hough_line_peaks(*hough))]
        if not angles:
            log.warn("Image skew could not be calculated. The image is probably invalid.")
            return 0.0
        else:
            # Get the average angle and convert it to degrees
            offset = sum(angles) / len(angles) * 180.0 / math.pi
            if offset > V1Rotator.ACCEPTABLE_SKEW_THRESHOLD:
                log.warn("Image is heavily skewed. Check that the images are valid.")
            log.debug("Calculated rotation skew: %s" % offset)
            return offset
