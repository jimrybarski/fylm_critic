from fylm.model.device import Device
from fylm.model.image import Image
from fylm import stack, rotate
import logging
import numpy as np
import os
from skimage import transform, feature
from typing import Set, Tuple, Iterable, Dict


log = logging.getLogger(__name__)


class AdjustedImage(object):
    """
    Holds an image and the alignments that have been performed on it.

    """
    def __init__(self, image: Image, rotation: float, registration: Tuple[float, float]=None):
        self.image = image
        self.rotation = rotation
        self.registration = registration


def create_missing_rotated_images(brightfield_channel: str, device: Device, tif_filenames: Iterable[str],
                                  hdf5_filename: str, rotated_images: Dict[int, AdjustedImage]):
    rotation_calculator = _get_rotation_calculator(device)
    images = _load_primary_images(brightfield_channel, device, tif_filenames)
    with stack.ImageStack(hdf5_filename) as image_stack:
        for image, rotation in _make_rotated_missing_images(images, rotation_calculator):
            image_stack[image.index] = image
            image_stack[image.index].attrs['rotation'] = rotation
            rotated_images[image.field_of_view] = AdjustedImage(image, rotation)


def load_current_image_indices(hdf5_filename: str):
    with stack.ImageStack(hdf5_filename) as h5:
        return tuple(h5.keys())


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
        return transform.rotate(normalized_image, rotation), rotation


def load_new_nonfirst_brightfield_focused_images(tif_filenames: Iterable[str], brightfield_channel: str, current_indices: tuple):
    for tif_filename in tif_filenames:
        with stack.TiffReader(tif_filename) as tif:
            for raw_image in tif:
                if raw_image.channel != brightfield_channel or raw_image.z_offset != 0 or raw_image.frame == 0 or raw_image.index in current_indices:
                    continue
                yield raw_image


def _get_rotation_calculator(device: Device) -> rotate.RotationCalculator:
    calculator = {device.original: rotate.FYLMRotationCalc,
                  device.plinko: rotate.PlinkoRotationCalc,
                  device.cerevisiae: rotate.CerevisiaeRotationCalc,
                  device.hexaplex: rotate.FYLMRotationCalc}
    return calculator[device](device)


def _load_primary_images(brightfield_channel: str, device: Device, tif_filenames: Iterable[str]) -> Iterable[Image]:
    for tif_filename in tif_filenames:
        with stack.TiffReader(tif_filename) as tif:
            for raw_image in tif:
                is_primary_image = raw_image.frame == 0 and raw_image.z_offset == 0 and raw_image.channel == brightfield_channel
                if is_primary_image:
                    normalized_image = _normalize_image(raw_image, device)
                    yield Image(normalized_image, raw_image.frame, raw_image.timestamp,
                                raw_image.field_of_view, raw_image.channel, raw_image.z_offset)


def load_fields_of_view(tif_filenames: Iterable[str]) -> set:
    fields_of_view = set()
    for tif_filename in tif_filenames:
        with stack.TiffReader(tif_filename) as tif:
            index_map = tif.micromanager_metadata['index_map']
            for fov in index_map['position']:
                fields_of_view.add(int(fov))
    return fields_of_view


def load_tifs_filenames(tif_directory: str) -> Iterable[str]:
    tifs = tuple([os.path.join(tif_directory, tif) for tif in os.listdir(tif_directory) if tif.endswith('.ome.tif')])
    if len(tifs) == 0:
        raise ValueError("No TIFFs were found! "
                         "We need them in the preprocessing step to know if the HDF5 file has "
                         "all the fields of view!")
    return tifs


def load_existing_rotations(hdf5_filename: str, fields_of_view: Set[int], brightfield_channel: str) -> Dict[int, AdjustedImage]:
    # we're only concerned with rotations for now, and not registrations, because all registrations
    # are based on the first image

    # build up a dictionary of all first images, starting with the h5 data first
    # if we still don't have all of them, get the raw data from the TIFs
    rotated_images = {}
    with stack.ImageStack(hdf5_filename) as h5:
        for fov in fields_of_view:
            try:
                image = h5.get_image(fov, brightfield_channel, 0, 0)
                rotation = h5.get_attrs(fov, brightfield_channel, 0, 0).get('rotation')
                assert rotation is not None, "HDF5 is missing data: " \
                                             "it has images without rotation data in the metadata"
                rotated_images[fov] = AdjustedImage(image, rotation)
            except stack.ImageDoesNotExist:
                pass
    return rotated_images


def _normalize_image(image: np.ndarray, device: Device) -> np.ndarray:
    if device == Device.original:
        return crop(cw_rotate(image), 0.1)
    else:
        raise ValueError("Normalizing image not implemented for your device")


def cw_rotate(image: np.ndarray) -> np.ndarray:
    return np.flipud(image).T


def ccw_rotate(image: np.ndarray) -> np.ndarray:
    return np.flipud(image.T)


def crop(image: np.ndarray, margin_percent: float) -> np.ndarray:
    # sometimes we snag corners, by cropping the left and right 10% of the image we focus only on the
    # vertical bars formed by the structure
    height, width = image.shape
    margin = int(width * margin_percent)
    return image[:, margin: width - margin]
