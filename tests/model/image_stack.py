import unittest
from model.image.stack import ImageStack


class MockImage(object):
    def __init__(self, field_of_view=0):
        self.data = "image_data"
        self.field_of_view = field_of_view

class ImageStackTests(unittest.TestCase):
    def test_add_correct_length(self):
        """ Does adding image sets result in the correct length for the stack? """
        stack = ImageStack()
        image_set = {"1": 1, "2": 2}
        image_set2 = {"1": 1, "2": 2, "3": 3}
        stack.add(image_set)
        self.assertEqual(len(stack), 2)
        stack.add(image_set2)
        self.assertEqual(len(stack), 5)

    def test_add(self):
        stack = ImageStack()
        image_set = {"1": 1, "2": 2}
        image_set2 = {"1": 1, "2": 2, "3": 3}
        stack.add(image_set)
        stack.add(image_set2)
        self.assertListEqual(sorted(list(stack._image_lookup.keys())), [0, 1, 2, 3, 4])

    def test_getitem(self):
        """
        We combine several sets of images, each of which starts its own index at zero.
        We want to be able to combine them into one superset and have a single range of indices.

        """
        stack = ImageStack()
        image_set = {0: "image0", 1: "image1"}
        image_set2 = {0: "image2", 1: "image3", 2: "image4"}
        stack.add(image_set)
        stack.add(image_set2)
        self.assertEqual(stack[0], "image0")
        self.assertEqual(stack[1], "image1")
        self.assertEqual(stack[2], "image2")
        self.assertEqual(stack[3], "image3")
        self.assertEqual(stack[4], "image4")

    def test_iter(self):
        stack = ImageStack()
        image_set = {0: "image0", 1: "image1"}
        image_set2 = {0: "image2", 1: "image3", 2: "image4"}
        stack.add(image_set)
        stack.add(image_set2)
        images = [im for im in stack]
        self.assertEqual(len(images), 5)

    def test_filter(self):
        stack = ImageStack()
        image_set = {0: MockImage(field_of_view=0), 1: MockImage(field_of_view=1)}
        image_set2 = {0: MockImage(field_of_view=0), 1: MockImage(field_of_view=1), 2: MockImage(field_of_view=3)}
        stack.add(image_set)
        stack.add(image_set2)
        fov0 = [im for im in stack.filter(field_of_view=0)]
        fov1 = [im for im in stack.filter(field_of_view=1)]
        fov2 = [im for im in stack.filter(field_of_view=2)]
        fov3 = [im for im in stack.filter(field_of_view=3)]
        self.assertEqual(len(fov0), 2)
        self.assertEqual(len(fov1), 2)
        self.assertEqual(len(fov2), 0)
        self.assertEqual(len(fov3), 1)
