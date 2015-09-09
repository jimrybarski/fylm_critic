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
        image_set = {"1": 1, "2": 2}
        image_set2 = {"1": 1, "2": 2, "3": 3}
        stack.add(image_set)
        stack.add(image_set2)
        self.assertTupleEqual(stack[0], (0, 0))
        self.assertTupleEqual(stack[1], (0, 1))
        self.assertTupleEqual(stack[2], (1, 0))
        self.assertTupleEqual(stack[3], (1, 1))
        self.assertTupleEqual(stack[4], (1, 2))
