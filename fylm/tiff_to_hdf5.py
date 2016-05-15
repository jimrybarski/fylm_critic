from skimage import transform
from skimage.morphology import skeletonize
from skimage.filters import rank, threshold_otsu, sobel_v
from skimage.morphology import disk, remove_small_objects
from scipy import ndimage
import tifffile
import h5py
import math
import os
import warnings
# warnings.filterwarnings("ignore")
from datetime import datetime
import numpy as np
from fylm.image import ImageStack
from skimage import io
from fylm.model import constants
import logging
import statistics

log = logging.getLogger(__name__)




# with h5py.File("/var/fylm3/FYLM-160329.h5", "a") as h5:
#     directory = "/var/fylm3/ome files/FYLM-160329_1"
#     for filename in sorted(os.listdir(directory)):
#         tiff = tifffile.TiffFile(os.path.join(directory, filename))
#         pixel_size_um = tiff.micromanager_metadata['summary']['PixelSize_um']
#         for image in tiff:
#             data = image.tags['micromanager_metadata'].value
#             field_of_view = data['PositionIndex']
#             channel = data['Channel']
#             z_offset = data['SlicePosition']
#             width = data['Width']
#             height = data['Height']
#             frame = data['FrameIndex']
#             uuid = data['UUID']
#             timestamp = int(datetime.strptime(data['Time'], "%Y-%m-%d %H:%M:%S %z").timestamp())
#             exposure_ms = data['Exposure-ms']
#             print(filename, field_of_view, frame, channel, z_offset)
            # group = h5.require_group('/%d/%s/%d' % (field_of_view, channel, z_offset))
            # dataset = group.create_dataset(str(frame), (width, height), dtype=np.uint16)
            # transformed_image = np.flipud(image.asarray().T)
            # dataset[...] = transformed_image


def calculate_rotation(image):
    # sometimes we snag corners, by cropping the left and right 10% of the image we focus only on the
    # vertical bars formed by the structure
    height, width = image.shape
    crop = int(width * 0.1)
    cropped_image = image[:, crop: width - crop]
    # Find edges that have a strong vertical direction
    vertical_edges = sobel_v(cropped_image)
    # Separate out the areas where there is a large amount of vertically-oriented stuff
    segmentation = segment_edge_areas(vertical_edges)
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


def segment_edge_areas(edges, disk_size=9, mean_threshold=100, min_object_size=750):
    """
    Takes a greyscale image (with brighter colors corresponding to edges) and returns a binary image where white
    indicates an area with high edge density and black indicates low density.
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

if __name__ == '__main__':
    with h5py.File("/var/fylm3/FYLM-160329.h5") as hf:
        offsets = []
        for i in range(3):
            image = hf['/0/BF/0/'].get(str(i)).value
            offsets.append(calculate_rotation(image))
        offset = statistics.median(offsets)
        rotated_image = transform.rotate(hf['/0/BF/0/'].get('0'), offset)
        io.imshow(rotated_image)
        io.show()
