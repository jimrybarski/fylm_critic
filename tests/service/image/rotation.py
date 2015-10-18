import unittest
import numpy as np
from service.image.rotation import RotationCorrector, V1RotationAnalyzer
from model.image.rotation import RotationOffsets


class MockImage(np.ndarray):
    def __new__(cls, array, frame_number=5):
        return np.asarray(array).view(cls)

    def __init__(self, array, frame_number=5):
        self.frame_number = frame_number


class MockV1RotationAnalyzer(object):
    def __init__(self, fake_skew_values):
        self._fake_skew_values = fake_skew_values

    def _calculate_skew(self, image):
        return self._fake_skew_values.pop()


class FakeV1RotationAnalyzer(MockV1RotationAnalyzer, V1RotationAnalyzer):
    pass


class RotationTests(unittest.TestCase):
    def test_rotate(self):
        # just ensures that we're really rotating counterclockwise and that types are correct and such
        image = np.zeros((3, 3), dtype=np.bool)
        image[0][1] = 1
        image = MockImage(image)
        offsets = RotationOffsets()
        offsets[0] = 90.0
        rotated = RotationCorrector(offsets).adjust(image).astype(np.bool)
        expected = np.zeros((3, 3), dtype=np.bool)
        expected[1][0] = 1
        # test if the arrays are equal
        self.assertFalse((rotated - expected).any())


class V1RotationAnalyzerTests(unittest.TestCase):
    def setUp(self):
        self.analyzer = FakeV1RotationAnalyzer([4.0, 3.0, 2.0, 1.7])

    def test_get_start_frame(self):
        offsets = RotationOffsets()
        self.assertIsNone(offsets.last_real_value)
        offsets[0] = 90.0
        self.assertEqual(0, offsets.last_real_value)
        offsets[27] = 180.0
        self.assertEqual(27, offsets.last_real_value)

    def test_calculate_offsets(self):
        offsets = RotationOffsets()
        image = np.zeros((3, 3), dtype=np.bool)
        image_stack = [MockImage(image, frame_number=i) for i in range(100)]
        self.analyzer._calculate_offsets(image_stack, 0, 25, offsets)
        self.assertEqual(offsets[0], 1.7)
        self.assertEqual(offsets[24], 1.7)
        self.assertEqual(offsets[25], 2.0)
        self.assertEqual(offsets[49], 2.0)
        self.assertEqual(offsets[50], 3.0)
        self.assertEqual(offsets[65], 3.0)
        self.assertEqual(offsets[75], 4.0)
        self.assertEqual(offsets[98], 4.0)
        self.assertEqual(offsets[99], 4.0)

    def test_calculate_offsets_some_work_done(self):
        offsets = RotationOffsets()
        offsets[0] = 1.0
        offsets[25] = 2.0
        offsets[50] = 3.0
        image = np.zeros((3, 3), dtype=np.bool)
        image_stack = [MockImage(image, frame_number=i) for i in range(100)]
        self.analyzer._calculate_offsets(image_stack, 75, 25, offsets)
        self.assertEqual(offsets[0], 1.0)
        self.assertEqual(offsets[24], 1.0)
        self.assertEqual(offsets[25], 2.0)
        self.assertEqual(offsets[49], 2.0)
        self.assertEqual(offsets[50], 3.0)
        self.assertEqual(offsets[65], 3.0)
        self.assertEqual(offsets[75], 1.7)
        self.assertEqual(offsets[98], 1.7)
        self.assertEqual(offsets[99], 1.7)

    def test_determine_offsets(self):
        offsets = RotationOffsets()
        image = np.zeros((3, 3), dtype=np.bool)
        image_stack = [MockImage(image, frame_number=i) for i in range(100)]
        self.analyzer.determine_offsets(image_stack, offsets, 25)
        self.assertEqual(offsets[0], 1.7)
        self.assertEqual(offsets[24], 1.7)
        self.assertEqual(offsets[25], 2.0)
        self.assertEqual(offsets[49], 2.0)
        self.assertEqual(offsets[50], 3.0)
        self.assertEqual(offsets[65], 3.0)
        self.assertEqual(offsets[75], 4.0)
        self.assertEqual(offsets[98], 4.0)
        self.assertEqual(offsets[99], 4.0)

    def test_determine_offsets_some_work_done(self):
        offsets = RotationOffsets()
        offsets[0] = 1.0
        offsets[25] = 2.0
        offsets[50] = 3.0
        image = np.zeros((3, 3), dtype=np.bool)
        image_stack = [MockImage(image, frame_number=i) for i in range(100)]
        self.analyzer.determine_offsets(image_stack, offsets, 25)
        self.assertEqual(offsets[0], 1.0)
        self.assertEqual(offsets[24], 1.0)
        self.assertEqual(offsets[25], 2.0)
        self.assertEqual(offsets[49], 2.0)
        self.assertEqual(offsets[50], 3.0)
        self.assertEqual(offsets[65], 3.0)
        self.assertEqual(offsets[75], 1.7)
        self.assertEqual(offsets[98], 1.7)
        self.assertEqual(offsets[99], 1.7)

    def test_determine_offsets_all_work_done(self):
        offsets = RotationOffsets()
        offsets[0] = 9.0
        offsets[25] = 9.0
        offsets[50] = 9.0
        offsets[75] = 9.0
        image = np.zeros((3, 3), dtype=np.bool)
        image_stack = [MockImage(image, frame_number=i) for i in range(100)]
        self.analyzer.determine_offsets(image_stack, offsets, 25)
        self.assertEqual(offsets[0], 9.0)
        self.assertEqual(offsets[24], 9.0)
        self.assertEqual(offsets[25], 9.0)
        self.assertEqual(offsets[49], 9.0)
        self.assertEqual(offsets[50], 9.0)
        self.assertEqual(offsets[65], 9.0)
        self.assertEqual(offsets[75], 9.0)
        self.assertEqual(offsets[98], 9.0)
        self.assertEqual(offsets[99], 9.0)

