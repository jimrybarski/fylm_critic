"""
Methods to determine how much an image needs to be rotated in order to be "upright". We have several
devices, each of which use a different algorithm. Currently these are hand written, though it may be
worth looking into a neural network or something more advanced.

"""
from skimage import transform
from skimage.morphology import skeletonize
from skimage.filters import rank, threshold_otsu, sobel_v
from skimage.morphology import disk, remove_small_objects
from scipy import ndimage
import math
from fylm.model import constants
from fylm.model.device import Device
import numpy as np
import logging
from abc import abstractmethod

log = logging.getLogger(__name__)


class RotationCalculator(object):
    @abstractmethod
    def calculate(self, *args, **kwargs) -> float:
        raise NotImplementedError


class FYLMRotationCalc(RotationCalculator):
    """
    Finds the degrees counterclockwise that we need to rotate the image to make it upright.
    Works for standard FYLM devices with 28 catch tubes.

    """
    def __init__(self, device: Device):
        assert device in (Device.original, Device.hexaplex)

    def calculate(self, image: np.ndarray, disk_size: int=9,
                  mean_threshold: int=100, min_object_size: int=750) -> float:
        # Find edges that have a strong vertical direction
        vertical_edges = sobel_v(image)
        # Separate out the areas where there is a large amount of vertically-oriented stuff
        segmentation = self._segment_edge_areas(vertical_edges, disk_size, mean_threshold, min_object_size)
        # Draw a line that follows the center of the segments at each point, which should be roughly vertical
        # We should expect this to give us four approximately-vertical lines, possibly with many gaps in
        # each line
        skeletons = skeletonize(segmentation)
        # Use the Hough transform to get the closest lines that approximate those four lines
        hough = transform.hough_line(skeletons, np.arange(-constants.FIFTEEN_DEGREES_IN_RADIANS,
                                                          constants.FIFTEEN_DEGREES_IN_RADIANS,
                                                          0.0001))
        # Create a list of the angles (in radians) of all of the lines the Hough transform produced, with 0.0
        # being completely vertical
        # These angles correspond to the angles of the four sides of the channels, which we need to
        # correct for
        angles = [angle for _, angle, dist in zip(*transform.hough_line_peaks(*hough))]
        if not angles:
            raise ValueError("Image rotation could not be calculated. Check the images to see if they're weird.")
        else:
            # Get the average angle and convert it to degrees
            offset = sum(angles) / len(angles) * 180.0 / math.pi
            if offset > constants.ACCEPTABLE_SKEW_THRESHOLD:
                log.warn("Image is heavily skewed. Check that the images are valid.")
            return offset

    def _segment_edge_areas(self, edges, disk_size, mean_threshold, min_object_size):
        """
        Takes a greyscale image (with brighter colors corresponding to edges) and returns a
        binary image where white indicates an area with high edge density and black indicates low density.
        """
        # Convert the greyscale edge information into black and white (ie binary) image
        threshold = threshold_otsu(edges)
        # Filter out the edge data below the threshold, effectively removing some noise
        raw_channel_areas = edges <= threshold
        # Smooth out the data
        channel_areas = rank.mean(raw_channel_areas, disk(disk_size)) < mean_threshold
        # Remove specks and blobs that are the result of artifacts
        clean_channel_areas = remove_small_objects(channel_areas, min_size=min_object_size)
        # Fill in any areas that are completely surrounded by the areas (hopefully) covering the channels
        return ndimage.binary_fill_holes(clean_channel_areas)


class PlinkoRotationCalc(RotationCalculator):
    """
    Finds the degrees counterclockwise that we need to rotate the image to make it upright.
    Works for Pombe plinko devices.

    """
    def __init__(self, device: Device):
        assert device == Device.plinko

    def calculate(self, image: np.ndarray) -> float:
        raise NotImplementedError("Jim hasn't written a method to process plinko images yet")


class CerevisiaeRotationCalc(RotationCalculator):
    """
    Finds the degrees counterclockwise that we need to rotate the image to make it upright.
    Works for Cerevisiae devices.

    """
    def __init__(self, device: Device):
        assert device == Device.cerevisiae

    def calculate(self, image: np.ndarray) -> float:
        raise NotImplementedError("Jim hasn't written a method to process cerevisiae images yet")
