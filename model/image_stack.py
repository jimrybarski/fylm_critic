class ImageStack(object):
    """
    This is a model that combines multiple ND2s into one logical image set. Other file types may be used if they are in an object that exposes
    images via __getitem__ and defines __len__ as the number of images.

    """
    def __init__(self):
        self._image_sets = {}
        self._image_lookup = {}

    def add(self, image_set):
        """ Adds a set of images to the virtual image stack. """
        # ensure the image set is valid
        if not (hasattr(image_set, "__getitem__") and hasattr(image_set, "__len__")):
            raise TypeError("You tried to add an image set to the ImageStack but it doesn't provide the right interface (__getitem__ and __len__)")
        # the index is the range of frame numbers
        image_set_index = len(self._image_sets)
        image_count = len(self._image_lookup)
        for i in range(len(image_set)):
            self._image_lookup[image_count + i] = (image_set_index, i)
        self._image_sets[image_set_index] = image_set

    def __len__(self):
        return len(self._image_lookup)

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError("ImageStack uses integer indexes only.")
        if item < 0 or item >= len(self):
            raise ValueError("Out of bounds index access for ImageStack")
        image_set_index, image_index = self._image_lookup[item]
        return self._image_sets[image_set_index][image_index]