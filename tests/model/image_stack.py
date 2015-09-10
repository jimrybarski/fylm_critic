import unittest
from model.image_stack import ImageStack


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
