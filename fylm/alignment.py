from fylm.model.device import Device
from fylm.model.image import Image, LazyTif
from fylm.rotate import RotationCalculator
from fylm import stack, rotate
from fylm import image as fimage
import logging
import os
import numpy as np
from skimage import transform, feature
from typing import Set, Tuple, Iterable, Dict


log = logging.getLogger(__name__)


class AdjustedImage(object):
    """
    Holds an image and the alignments that have been performed on it.

    """
    def __init__(self, image: Image, rotation: float, registration: Tuple[float, float]=(0, 0)):
        self.image = image
        self.rotation = rotation
        self.registration = registration


def create_missing_rotated_images(brightfield_channel: str,
                                  device: Device,
                                  tifs: Iterable[LazyTif],
                                  image_stack: stack.ImageStack,
                                  rotation_calculator: RotationCalculator,
                                  rotated_images: Dict[int, AdjustedImage]):
    normalized_primary_images = _get_normalized_primary_images(brightfield_channel, device, tifs)
    for image, rotation in _make_rotated_missing_images(normalized_primary_images, rotation_calculator):
        image_stack[image.index] = image
        image_stack[image.index].attrs['rotation'] = rotation
        image_stack[image.index].attrs['registration'] = (0.0, 0.0)
        rotated_images[image.field_of_view] = AdjustedImage(image, rotation)


def _get_normalized_primary_images(brightfield_channel: str,
                                   device: Device,
                                   tifs: Iterable[LazyTif]) -> Iterable[Image]:
    for tif in tifs:
        is_primary_image = tif.frame == 0 and tif.z_offset == 0 and tif.channel == brightfield_channel
        if is_primary_image:
            normalized_image = _normalize_image(tif.image_data, device)
            yield Image(normalized_image, tif.frame, tif.timestamp,
                        tif.field_of_view, tif.channel, tif.z_offset)


def make_registered_image(image: Image,
                          device: Device,
                          rotation: float,
                          source_image: np.ndarray) -> AdjustedImage:
    normalized_image = _normalize_image(image, device)
    rotated_image = transform.rotate(normalized_image, rotation)
    (y, x), error, phase = feature.register_translation(source_image,
                                                        rotated_image,
                                                        upsample_factor=20)
    registered_image = transform.warp(rotated_image, transform.AffineTransform(translation=(-x, -y)))
    return AdjustedImage(Image(registered_image, image.frame, image.timestamp,
                               image.field_of_view, image.channel, image.z_offset),
                         rotation,
                         (x, y))


def _make_rotated_missing_images(images: Iterable[Image],
                                 rotation_calculator: rotate.RotationCalculator) -> Tuple[Image, float]:
    # precision rotate the image into the correct orientation.
    for normalized_image in images:
        # calculate how much we should rotate the image
        rotation = rotation_calculator.calculate(normalized_image)
        return Image.combine(transform.rotate(normalized_image, rotation), normalized_image), rotation


def get_new_nonfirst_brightfield_focused_images(tifs: Iterable[LazyTif],
                                                brightfield_channel: str,
                                                image_stack: stack.ImageStack):
    # Loads TIFs if they're not already in the HDF5.
    for tif in tifs:
        current_indices = image_stack.indices(tif.field_of_view, tif.channel, tif.z_offset)
        if tif.channel != brightfield_channel or tif.z_offset != 0 or tif.frame == 0 or tif.index in current_indices:
            continue
        yield tif


def get_rotation_calculator(device: Device) -> rotate.RotationCalculator:
    calculator = {device.original: rotate.FYLMRotationCalc,
                  device.plinko: rotate.PlinkoRotationCalc,
                  device.cerevisiae: rotate.CerevisiaeRotationCalc,
                  device.hexaplex: rotate.FYLMRotationCalc}
    return calculator[device](device)


def get_fields_of_view(tifs: Iterable[LazyTif]) -> set:
    return {tif.field_of_view for tif in tifs}


def load_tifs(tif_directory: str) -> Iterable[LazyTif]:
    tifs = tuple([os.path.join(tif_directory, tif) for tif in os.listdir(tif_directory) if tif.endswith('.ome.tif')])
    if len(tifs) == 0:
        raise ValueError("No TIFFs were found! "
                         "We need them in the preprocessing step to know if the HDF5 file has "
                         "all the fields of view!")
    for tif_filename in tifs:
        with stack.TiffReader(tif_filename) as tif:
            yield from tif


def get_existing_rotations(image_stack: stack.ImageStack,
                           fields_of_view: Set[int],
                           brightfield_channel: str) -> Dict[int, AdjustedImage]:
    # we're only concerned with rotations for now, and not registrations, because all registrations
    # are based on the first image

    # build up a dictionary of all first images, starting with the h5 data first
    # if we still don't have all of them, get the raw data from the TIFs
    rotated_images = {}
    for fov in fields_of_view:
        try:
            image = image_stack.get_image(fov, brightfield_channel, 0, 0)
            rotation = image_stack.get_attrs(fov, brightfield_channel, 0, 0).get('rotation')
            assert rotation is not None, "HDF5 is missing data: " \
                                         "it has images without rotation data in the metadata"
            rotated_images[fov] = AdjustedImage(image, rotation)
        except stack.ImageDoesNotExist:
            pass
    return rotated_images


def _normalize_image(image: np.ndarray, device: Device) -> np.ndarray:
    if device == Device.original:
        return fimage.crop(fimage.cw_rotate(image), 0.1)
    else:
        raise ValueError("Normalizing image not implemented for your device")
