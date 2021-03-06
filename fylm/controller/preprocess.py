"""
Preprocesses raw image data to create an HDF5 file with metadata. This is intended to be run while data
is being acquired, and should work incrementally. This way, we can run analyses while the experiment
is underway and determine automatically if we should stop.

"""
from fylm import stack, alignment
from fylm.model.device import Device
import logging

log = logging.getLogger(__name__)


def main(tif_directory: str, hdf5_filename: str, device: Device, brightfield_channel: str='BF'):
    # build up a set of all the fields of view
    tifs = alignment.load_tifs(tif_directory)
    fields_of_view = alignment.get_fields_of_view(tifs)

    with stack.ImageStack(hdf5_filename) as image_stack:
        rotated_images = alignment.get_existing_rotations(image_stack, fields_of_view, brightfield_channel)
        missing_first_images = len(fields_of_view) > len(rotated_images)
        if missing_first_images:
            log.debug("Calculating rotations for some images.")
            tifs = alignment.load_tifs(tif_directory)
            rotation_calculator = alignment.get_rotation_calculator(device)
            alignment.create_missing_rotated_images(brightfield_channel, device, tifs, image_stack,
                                                    rotation_calculator, rotated_images)

        # Go back and make sure we have all the registered images
        tifs = alignment.load_tifs(tif_directory)
        signal_registration = True
        for tif in alignment.get_new_nonfirst_brightfield_focused_images(tifs,
                                                                           brightfield_channel,
                                                                           image_stack):
            if signal_registration:
                log.debug("Registering images.")
            signal_registration = False

            rotation = rotated_images[tif.field_of_view].rotation
            source_image = rotated_images[tif.field_of_view].image
            registered_image = alignment.make_registered_image(tif.as_image, device, rotation, source_image)
            image_stack[tif.index] = registered_image.image
            image_stack[tif.index].attrs['rotation'] = registered_image.rotation
            image_stack[tif.index].attrs['registration'] = registered_image.registration
    log.debug("Done creating aligned images.")
