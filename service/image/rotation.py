import logging
import math
import numpy as np
from scipy import ndimage
from skimage.filters import gaussian_filter, rank, threshold_otsu, sobel_v
from skimage.morphology import disk, remove_small_objects, skeletonize
from skimage import transform
from model.image.offset import RotationOffsets
from skimage import io

FIFTEEN_DEGREES_IN_RADIANS = 0.262

log = logging.getLogger(__name__)


class RotationCorrector(object):
    """
    Takes images that are rotated in the XY-plane and corrects them.

    """
    def __init__(self, offsets):
        self._offsets = offsets

    def adjust(self, image):
        return self._rotate(image, self._offsets.get(image.field_of_view))

    @staticmethod
    def _rotate(image: np.array, degrees: float) -> np.array:
        return transform.rotate(image, degrees)


class V1RotationAnalyzer(object):
    FIELD_OF_VIEW_COUNT = 8

    def determine_offsets(self, image_stack, offsets: RotationOffsets, brightfield_channel_name: str) -> RotationOffsets:
        # We may only be partially done determining offsets. We'll pick up where we left off (or start at the beginning)
        self._calculate_offsets(image_stack, offsets, brightfield_channel_name)

    def _calculate_offsets(self, image_stack, offsets, brightfield_channel_name):
        # we still have some work to do
        for unrotated_image in image_stack.filter(z_level=1, channel=brightfield_channel_name):
            skew = self._calculate_skew(unrotated_image)
            offsets.set(unrotated_image.field_of_view, skew)
            if len(offsets) == V1RotationAnalyzer.FIELD_OF_VIEW_COUNT:
                break

    @staticmethod
    def _calculate_skew(image: np.array) -> float:
        """
        Determines the rotational skew of an image of a Version 1 FYLM device (the one with 28 channels per field of
        view and a large central trench.

        """
        acceptable_skew_threshold = 5.0
        vertical_edges = sobel_v(image)
        # Convert the greyscale edge information into black and white (ie binary) image
        threshold = threshold_otsu(vertical_edges)
        # Filter out the edge data below the threshold, effectively removing some noise
        raw_channel_areas = vertical_edges <= threshold
        # Smooth out the data
        # channel_areas = rank.mean(raw_channel_areas, disk(9))
        channel_areas = gaussian_filter(raw_channel_areas, 2)
        io.imshow(channel_areas)
        io.show()
        # Remove specks and blobs that are the result of artifacts
        clean_channel_areas = remove_small_objects(channel_areas < 50, min_size=500)
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
            return None
        else:
            # Get the average angle and convert it to degrees
            offset = sum(angles) / len(angles) * 180.0 / math.pi
            if offset > acceptable_skew_threshold:
                log.warn("Image is heavily skewed. Check that the images are valid.")
            log.debug("Calculated rotation skew: %s" % offset)
            return offset
