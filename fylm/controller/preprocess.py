"""
Preprocesses raw image data to create an HDF5 file with metadata. This is intended to be run while data
is being acquired, and should work incrementally. This way, we can run analyses while the experiment
is underway and determine automatically if we should stop.

"""
from fylm import stack, alignment, rotate
from fylm.model.device import Device
import os
from skimage import transform, feature
from typing import Set, Tuple
from fylm.stack import ImageDoesNotExist


def main(tif_directory: str, hdf5_filename: str, device: Device, brightfield_channel: str='BF'):
    # build up a set of all the fields of view
    tif_filenames = _load_tifs_filenames(tif_directory)
    fields_of_view = _load_fields_of_view(tif_filenames)
    first_images, rotations = _load_existing_rotations(hdf5_filename, fields_of_view, brightfield_channel)

    missing_first_images = any([image is None for image in first_images.values()])
    if missing_first_images:
        # precision rotate the image into the correct orientation.
        rotation_calculator = _get_rotation_calculator(device)

        with stack.ImageStack(hdf5_filename) as h5:
            for tif_filename in tif_filenames:
                with stack.TiffReader(tif_filename) as tif:
                    for raw_image in tif:
                        primary_image = raw_image.frame == 0 and raw_image.z_offset == 0 and raw_image.channel == brightfield_channel
                        if not primary_image:
                            continue
                        # calculate how much we should rotate the image
                        normalized_image = alignment.normalize_image(raw_image, device)
                        rotation = rotation_calculator.calculate(normalized_image)
                        rotations[raw_image.field_of_view] = rotation

                        # rotate the image and add it to the HDF5
                        rotated_image = transform.rotate(normalized_image, rotation)
                        first_images[raw_image.field_of_view] = rotated_image
                        index = _format_index(raw_image.field_of_view,
                                              raw_image.frame,
                                              raw_image.channel,
                                              raw_image.z_offset)
                        h5[index] = rotated_image
                        h5[index].attrs['rotation'] = rotation
                        break

    registrations = {}
    # Go back and make sure we have all the registered images
    with stack.ImageStack(hdf5_filename) as h5:
        for tif_filename in tif_filenames:
            with stack.TiffReader(tif_filename) as tif:
                for raw_image in tif:
                    if raw_image.channel != brightfield_channel or raw_image.z_offset != 0 or raw_image.frame == 0:
                        continue
                    index = _format_index(raw_image.field_of_view,
                                          raw_image.frame,
                                          raw_image.channel,
                                          raw_image.z_offset)
                    if index not in h5.keys():
                        normalized_image = alignment.normalize_image(raw_image, device)
                        rotated_image = transform.rotate(normalized_image, rotations[raw_image.field_of_view])
                        image = first_images[raw_image.field_of_view]
                        (y, x), error, phase = feature.register_translation(image,
                                                                            rotated_image,
                                                                            upsample_factor=20)
                        registrations[index] = x, y


def _load_fields_of_view(tif_filenames: Tuple[str]) -> set:
    fields_of_view = set()
    for tif_filename in tif_filenames:
        with stack.TiffReader(tif_filename) as tif:
            index_map = tif.micromanager_metadata['index_map']
            for fov in index_map['position']:
                fields_of_view.add(fov)
    return fields_of_view


def _get_rotation_calculator(device: Device) -> rotate.RotationCalculator:
    calculator = {device.original: rotate.FYLMRotationCalc,
                  device.plinko: rotate.PlinkoRotationCalc,
                  device.cerevisiae: rotate.CerevisiaeRotationCalc,
                  device.hexaplex: rotate.FYLMRotationCalc}
    return calculator[device](device)


def _format_index(fov: int, frame: int, channel: str, z_level: int) -> str:
    return '%d/%d/%s/%d' % (fov, frame, channel, z_level)


def _load_tifs_filenames(tif_directory: str) -> [str]:
    tifs = tuple([os.path.join(tif_directory, tif) for tif in os.listdir(tif_directory) if tif.endswith('.ome.tif')])
    if len(tifs) == 0:
        raise ValueError("No TIFFs were found! "
                         "We need them in the preprocessing step to know if the HDF5 file has "
                         "all the fields of view!")
    return tifs


def _load_existing_rotations(hdf5_filename: str, fields_of_view: Set[str], brightfield_channel: str) -> Tuple[dict, dict]:
    # we're only concerned with rotations for now, and not registrations, because all registrations
    # are based on the first image
    rotations = {}
    # build up a dictionary of all first images, starting with the h5 data first
    # if we still don't have all of them, get the raw data from the TIFs
    first_images = {fov: None for fov in fields_of_view}
    with stack.ImageStack(hdf5_filename) as h5:
        for fov in fields_of_view:
            try:
                first_images[fov] = h5.get_image(fov, brightfield_channel, 0, 0)
                rotations[fov] = h5.get_attrs(fov, brightfield_channel, 0, 0).get('rotation')
                assert rotations[fov] is not None, 'HDF5 is missing data: ' \
                                                   'it has images without rotation data in the metadata'
            except ImageDoesNotExist:
                pass
    return first_images, rotations
