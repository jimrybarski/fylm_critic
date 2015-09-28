class ImageStack(object):
    """
    This is a model that combines multiple ND2s into one logical image set. Other file types may be used if they are in an object that exposes
    images via __getitem__ and defines __len__ as the number of images.

    """
    def __init__(self):
        self._image_sets = {}
        self._image_lookup = {}
        self._translator = None
        self._rotator = None
        self._field_of_view = None
        self._z_level = None
        self._channel = None

    def add(self, image_set):
        """ Adds a set of images to the virtual image stack. The order that sets are added determines the order of the final stack! """
        # ensure the image set is valid
        if not (hasattr(image_set, "__getitem__") and hasattr(image_set, "__len__")):
            raise TypeError("You tried to add an image set to the ImageStack but it doesn't provide the right interface (__getitem__ and __len__)")
        # we need a new slot in our _image_sets dictionary for the new image set we've just been given
        # since we want the last index plus one, we can just use the length of _image_sets
        image_set_index = len(self._image_sets)
        # we need to know how many total images we already have, so when we index the new images in the new image set,
        # we can start from the next available index
        image_count = len(self._image_lookup)
        # We use range(len()) instead of iteration over the image set to avoid reading any data from disk
        for i in range(len(image_set)):
            # for each image, we create a new global index number, and map that to the particular image set it came from and its local index number
            self._image_lookup[image_count + i] = (image_set_index, i)
        # here we just store the image set so we can access the images from it
        self._image_sets[image_set_index] = image_set

    def __len__(self) -> int:
        """ The number of total images there are in all the image sets. """
        return len(self._image_lookup)

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError("ImageStack uses integer indexes only.")
        if not 0 <= index < len(self):
            raise IndexError("Out of bounds index access for ImageStack")
        # We have several sets of images, each indexed from 0 to some arbitrary number. We need to figure out which image set the given index maps to
        # Once we know the image set, we also need to know which image we should use
        image_set_index, image_index = self._image_lookup[index]
        return self._image_sets[image_set_index][image_index]

    def filter(self, field_of_view: int=None, z_level: int=None, channel: str=None):
        """ Returns an iterator over images that meet the given criteria. """
        _filter_function = lambda image: (field_of_view is None or image.field_of_view == field_of_view) and \
                                         (z_level is None or image.z_level == z_level) and \
                                         (channel is None or image.channel == channel)
        return filter(_filter_function, self)
