import unittest
from model.stack import ImageStack


class MockImage(object):
    def __init__(self, field_of_view=0):
        self.data = "image_data"
        self.field_of_view = field_of_view


class ImageStackTests(unittest.TestCase):
    def test_add_correct_length(self):
        # Does adding image sets result in the correct length for the stack?
        stack = ImageStack()
        image_set = {"1": 1, "2": 2}
        image_set2 = {"1": 1, "2": 2, "3": 3}
        stack.add(image_set)
        self.assertEqual(len(stack), 2)
        stack.add(image_set2)
        self.assertEqual(len(stack), 5)

    def test_add(self):
        # Can we add more images and have them get the correct indexes?
        stack = ImageStack()
        image_set = {"1": 1, "2": 2}
        image_set2 = {"1": 1, "2": 2, "3": 3}
        stack.add(image_set)
        stack.add(image_set2)
        self.assertListEqual(sorted(list(stack._image_lookup_table.keys())), [0, 1, 2, 3, 4])

    def test_getitem(self):
        # Can we combine multiple image sets and index into them properly?
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
        # Can we iterate over several different image sets and have it seem like there's just one?
        stack = ImageStack()
        image_set = {0: "image0", 1: "image1"}
        image_set2 = {0: "image2", 1: "image3", 2: "image4"}
        stack.add(image_set)
        stack.add(image_set2)
        images = [im for im in stack]
        self.assertEqual(len(images), 5)
