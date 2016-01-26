from nd2reader.model import Image


class ImageStack(object):
    """
    This is a model that combines multiple ND2s into one logical image set. Other file types may be used if they are in
    an object that exposes the same interface as nd2reader.

    """
    def __init__(self):
        self._image_sets = {}
        self._image_lookup_table = {}
        self._groups = {}
        self._registration_corrector = None
        self._rotation_corrector = None

    def set_correctors(self, registration_corrector=None, rotation_corrector=None):
        self._registration_corrector = registration_corrector
        self._rotation_corrector = rotation_corrector

    def add(self, image_set):
        """
        Adds a set of images to the virtual image stack. Image sets are typically a single ND2 file.
        The order that sets are added determines the order of the final stack!

        """
        # ensure the image set is valid
        if not (hasattr(image_set, "__getitem__") and hasattr(image_set, "__len__")):
            raise TypeError("You tried to add an image set to the ImageStack,"
                            " but it doesn't provide the right interface (__getitem__ and __len__)")
        # we need a new slot in our _image_sets dictionary for the new image set we've just been given
        # since we want the last index plus one, we can just use the length of _image_sets
        image_set_index = len(self._image_sets)
        # we need to know how many total images we already have, so when we index the new images in the new image set,
        # we can start from the next available index
        image_count = len(self._image_lookup_table)
        # We will keep track of groups of images. At each field of view, images with unique combinations of channel and
        # focus are taken together. Then we move on to another field of view, which is considered another group.
        # If we only have one field of view, a new group starts when an image has the same channel and focus as one in
        # the current group.
        for n in range(len(image_set)):
            # for each image, we create a new global index number, and map that to the particular image set it came
            # from and its local index number
            self._image_lookup_table[image_count + n] = (image_set_index, n)
        # here we just store the image set so we can access the images from it
        self._image_sets[image_set_index] = image_set

    @property
    def frame_count(self):
        return sum([len(image_set.frames) for image_set in self._image_sets.values()])

    @property
    def field_of_view_count(self):
        return len(self._image_sets[0].fields_of_view)

    def __len__(self) -> int:
        """ The number of total images there are in all the image sets. """
        return len(self._image_lookup_table)

    def _correct(self, image: Image) -> Image:
        """ Translates and rotates an image, if necessary. """
        if self._registration_corrector is None and self._rotation_corrector is None:
            return image
        # the correctors return numpy arrays so we need to capture this information before any transformations are done
        field_of_view = image.field_of_view
        frame_number = image.frame_number
        timestamp = image.timestamp
        index = image.index
        channel = image.channel
        z_level = image.z_level

        # make the corrections
        if self._registration_corrector is not None:
            image = self._registration_corrector.align(image, field_of_view, frame_number)
        if self._rotation_corrector is not None:
            image = self._rotation_corrector.rotate(image, field_of_view)
        corrected_image = Image(image)
        # add the metadata back
        corrected_image.add_params(index, timestamp, frame_number, field_of_view, channel, z_level)
        return corrected_image

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError("ImageStack uses integer indexes only.")
        if not 0 <= index < len(self):
            raise IndexError("Out of bounds index access for ImageStack")
        # We have several sets of images, each indexed from 0 to some arbitrary number. We need to figure out which
        # image set the given index maps to which file. Once we know the image set, we also need to know which image
        # we should use.
        image_set_index, image_index = self._image_lookup_table[index]
        return self._correct(self._image_sets[image_set_index][image_index])

    def select(self, fields_of_view: int=None, z_levels: int=None, channels: str=None):
        """ Returns an iterator over images that meet the given criteria. """
        for _, image_set in sorted(self._image_sets.items()):
            for image in image_set.select(fields_of_view=fields_of_view, z_levels=z_levels, channels=channels):
                yield self._correct(image)
