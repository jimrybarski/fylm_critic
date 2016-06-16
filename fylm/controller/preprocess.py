"""
Preprocesses raw image data to create an HDF5 file with metadata. This is intended to be run while data
is being acquired, and should work incrementally. This way, we can run analyses while the experiment
is underway and determine automatically if we should stop.

"""
from fylm import stack, alignment, rotate
from fylm.model.device import Device
from fylm.model.image import Image
import os
from skimage import transform, feature
from typing import Set, Tuple, Iterable, Dict
from fylm.stack import ImageDoesNotExist


class AdjustedImage(object):
    def __init__(self, image: Image, rotation: float, registration: Tuple[float, float]=None):
        self.image = image
        self.rotation = rotation
        self.registration = registration


def main(tif_directory: str, hdf5_filename: str, device: Device, brightfield_channel: str='BF'):
    # build up a set of all the fields of view
    tif_filenames = _load_tifs_filenames(tif_directory)
    fields_of_view = _load_fields_of_view(tif_filenames)
    rotated_images = _load_existing_rotations(hdf5_filename, fields_of_view, brightfield_channel)
    missing_first_images = len(fields_of_view) > len(rotated_images)
    if missing_first_images:
        create_missing_rotated_images(brightfield_channel, device, tif_filenames, hdf5_filename, rotated_images)

    # Go back and make sure we have all the registered images
    current_image_indices = _load_current_image_indices(hdf5_filename)
    with stack.ImageStack(hdf5_filename) as image_stack:
        for image in _get_new_nonfirst_brightfield_focused_images(tif_filenames,
                                                                  brightfield_channel,
                                                                  current_image_indices):
            registered_image = _get_registered_image(image, device, rotated_images)
            image_stack[image.index] = registered_image
            image_stack[image.index].attrs['rotation'] = image.rotation


def _load_current_image_indices(hdf5_filename: str):
    with stack.ImageStack(hdf5_filename) as h5:
        return tuple(h5.keys())


def _get_registered_image(image: Image,
                          device: Device,
                          rotated_images: Dict[int: AdjustedImage]) -> AdjustedImage:
    normalized_image = alignment.normalize_image(image, device)
    rotation = rotated_images[image.field_of_view].rotation
    rotated_image = transform.rotate(normalized_image, rotation)
    source_image = rotated_images[image.field_of_view].image
    (y, x), error, phase = feature.register_translation(source_image,
                                                        rotated_image,
                                                        upsample_factor=20)
    registered_image = transform.warp(rotated_image, transform.AffineTransform(translation=(-x, -y)))
    return AdjustedImage(Image(registered_image, image.frame, image.timestamp,
                               image.field_of_view, image.channel, image.z_offset),
                         rotation,
                         (x, y))


def _get_new_nonfirst_brightfield_focused_images(tif_filenames: Iterable[str], brightfield_channel: str, current_indices: tuple):
    for tif_filename in tif_filenames:
        with stack.TiffReader(tif_filename) as tif:
            for raw_image in tif:
                if raw_image.channel != brightfield_channel or raw_image.z_offset != 0 or raw_image.frame == 0 or raw_image.index in current_indices:
                    continue
                yield raw_image


def create_missing_rotated_images(brightfield_channel: str, device: Device, tif_filenames: Iterable[str],
                                  hdf5_filename: str, rotated_images: Dict[int: AdjustedImage]):
    rotation_calculator = _get_rotation_calculator(device)
    images = _load_primary_images(brightfield_channel, device, tif_filenames)
    with stack.ImageStack(hdf5_filename) as image_stack:
        for image, rotation in _get_rotated_missing_images(images, rotation_calculator):
            image_stack[image.index] = image
            image_stack[image.index].attrs['rotation'] = rotation
            rotated_images[image.field_of_view] = AdjustedImage(image, rotation)


def _get_rotated_missing_images(images: Iterable[Image], 
                                rotation_calculator: rotate.RotationCalculator) -> Tuple[Image, float]:
    # precision rotate the image into the correct orientation.
    for normalized_image in images:
        # calculate how much we should rotate the image
        rotation = rotation_calculator.calculate(normalized_image)
        return transform.rotate(normalized_image, rotation), rotation


def _load_primary_images(brightfield_channel: str, device: Device, tif_filenames: Iterable[str]) -> Iterable[Image]:
    for tif_filename in tif_filenames:
        with stack.TiffReader(tif_filename) as tif:
            for raw_image in tif:
                is_primary_image = raw_image.frame == 0 and raw_image.z_offset == 0 and raw_image.channel == brightfield_channel
                if is_primary_image:
                    normalized_image = alignment.normalize_image(raw_image, device)
                    yield Image(normalized_image, raw_image.frame, raw_image.timestamp, 
                                raw_image.field_of_view, raw_image.channel, raw_image.z_offset)


def _load_fields_of_view(tif_filenames: Iterable[str]) -> set:
    fields_of_view = set()
    for tif_filename in tif_filenames:
        with stack.TiffReader(tif_filename) as tif:
            index_map = tif.micromanager_metadata['index_map']
            for fov in index_map['position']:
                fields_of_view.add(int(fov))
    return fields_of_view


def _get_rotation_calculator(device: Device) -> rotate.RotationCalculator:
    calculator = {device.original: rotate.FYLMRotationCalc,
                  device.plinko: rotate.PlinkoRotationCalc,
                  device.cerevisiae: rotate.CerevisiaeRotationCalc,
                  device.hexaplex: rotate.FYLMRotationCalc}
    return calculator[device](device)


def _load_tifs_filenames(tif_directory: str) -> Iterable[str]:
    tifs = tuple([os.path.join(tif_directory, tif) for tif in os.listdir(tif_directory) if tif.endswith('.ome.tif')])
    if len(tifs) == 0:
        raise ValueError("No TIFFs were found! "
                         "We need them in the preprocessing step to know if the HDF5 file has "
                         "all the fields of view!")
    return tifs


def _load_existing_rotations(hdf5_filename: str, fields_of_view: Set[int], brightfield_channel: str) -> Dict[int: AdjustedImage]:
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
            except ImageDoesNotExist:
                pass
    return rotated_images
