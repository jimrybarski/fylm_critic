"""
Preprocesses raw image data to create an HDF5 file with metadata. This is intended to be run while data
is being acquired, and should work incrementally. This way, we can run analyses while the experiment
is underway and determine automatically if we should stop.

"""
from fylm import stack, alignment, rotate
from fylm.model.device import Device
import os
from skimage import transform
from skimage import feature


def main(tif_directory: str, hdf5_filename: str, device: Device):
    # build up a set of all the fields of view
    fields_of_view = set()
    for tif_filename in _load_tifs_filenames(tif_directory):
        with stack.TiffReader(tif_filename) as tif:
            index_map = tif.micromanager_metadata['index_map']
            for fov in index_map['position']:
                fields_of_view.add(fov)

    # build up a dictionary of all first images, starting with the h5 data first
    # if we still don't have all of them, get the raw data from the TIFs
    first_images = {fov: None for fov in fields_of_view}
    rotations = {}
    with stack.ImageStack(hdf5_filename) as h5:
        for fov in fields_of_view:
            try:
                first_images[fov] = h5.get_image(fov, 'BF', 0, 0)
                rotations[fov] = h5.get_attrs(fov, 'BF', 0, 0)['rotation']
            except KeyError:
                pass

    if any([i is None for i in first_images.values()]):
        calculator = {device.original: rotate.FYLMRotationCalc,
                      device.plinko: rotate.PlinkoRotationCalc,
                      device.cerevisiae: rotate.CerevisiaeRotationCalc,
                      device.hexaplex: rotate.FYLMRotationCalc}
        rotation_calculator = calculator[device](device)

        with stack.ImageStack(hdf5_filename) as h5:
            for tif_filename in _load_tifs_filenames(tif_directory):
                with stack.TiffReader(tif_filename) as tif:
                    for raw_image in tif:
                        if raw_image.frame == 0 and raw_image.z_offset == 0 and raw_image.channel == 'BF':
                            normalized_image = alignment.normalize_image(raw_image)
                            rotation = rotation_calculator.calculate(normalized_image)
                            rotations[raw_image.field_of_view] = rotation
                            rotated_image = transform.rotate(normalized_image, rotation)
                            first_images[raw_image.field_of_view] = rotated_image
                            # Save the images to the HDF5 file
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
        for tif_filename in _load_tifs_filenames(tif_directory):
            with stack.TiffReader(tif_filename) as tif:
                for raw_image in tif:
                    if raw_image.channel != 'BF' or raw_image.z_offset != 0 or raw_image.frame == 0:
                        continue
                    index = _format_index(raw_image.field_of_view,
                                          raw_image.frame,
                                          raw_image.channel,
                                          raw_image.z_offset)
                    if index not in h5.keys():
                        normalized_image = alignment.normalize_image(raw_image)
                        rotated_image = transform.rotate(normalized_image,
                                                         rotations[raw_image.field_of_view])
                        feature.register_translation(first_images[raw_image.field_of_view],
                                                     rotated_image,
                                                     upsample_factor=20)


def _format_index(fov, frame, channel, z_level):
    return '%d/%d/%s/%d' % (fov, frame, channel, z_level)


def _load_tifs_filenames(tif_directory: str) -> [str]:
    tifs = [os.path.join(tif_directory, tif) for tif in os.listdir(tif_directory) if tif.endswith('.ome.tif')]
    if len(tifs) == 0:
        raise ValueError("No TIFFs were found! "
                         "We need them in the preprocessing step to know if the HDF5 file has "
                         "all the fields of view!")
    yield from tifs
