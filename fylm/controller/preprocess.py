"""
Preprocesses raw image data to create an HDF5 file with metadata. This is intended to be run while data
is being acquired, and should work incrementally. This way, we can run analyses while the experiment
is underway and determine automatically if we should stop.

"""
from fylm import stack, alignment
from fylm.model.device import Device


def main(tif_directory: str, hdf5_filename: str, device: Device, brightfield_channel: str='BF'):
    # build up a set of all the fields of view
    tif_filenames = alignment.load_tifs_filenames(tif_directory)
    fields_of_view = alignment.load_fields_of_view(tif_filenames)
    rotated_images = alignment.load_existing_rotations(hdf5_filename, fields_of_view, brightfield_channel)
    missing_first_images = len(fields_of_view) > len(rotated_images)
    if missing_first_images:
        alignment.create_missing_rotated_images(brightfield_channel, device, tif_filenames, hdf5_filename, rotated_images)

    # Go back and make sure we have all the registered images
    current_image_indices = alignment.load_current_image_indices(hdf5_filename)
    with stack.ImageStack(hdf5_filename) as image_stack:
        for image in alignment.load_new_nonfirst_brightfield_focused_images(tif_filenames,
                                                                            brightfield_channel,
                                                                            current_image_indices):
            registered_image = alignment.make_registered_image(image, device, rotated_images)
            image_stack[image.index] = registered_image
            image_stack[image.index].attrs['rotation'] = image.rotation
