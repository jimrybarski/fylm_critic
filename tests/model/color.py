from model import color
from hypothesis import given
import hypothesis.strategies as st
import unittest
import numpy as np


class ColorTests(unittest.TestCase):
    def test_hex(self):
        self.assertEqual('#ff0003', color.Color(255, 0, 3).hex)

    @given(st.integers(min_value=0, max_value=255),
           st.integers(min_value=0, max_value=255),
           st.integers(min_value=0, max_value=255))
    def test_hex_values(self, r, g, b):
        h = color.Color(r, g, b).hex
        assert len(h) == 7
        assert isinstance(h, str)

    @given(st.integers(min_value=2, max_value=1024),
           st.integers(min_value=2, max_value=1024))
    def test_convert_to_rgb(self, rows, columns):
        image = np.random.randint(0, 65536, (rows, columns)).astype(np.uint16)
        color_image = color.convert_to_rgb(image)
        assert np.max(color_image) <= 255
        assert color_image.shape == (rows, columns, 3)

    @given(st.integers(min_value=2, max_value=1024),
           st.integers(min_value=2, max_value=1024),
           st.integers(min_value=0, max_value=255),
           st.integers(min_value=0, max_value=255),
           st.integers(min_value=0, max_value=255))
    def test_convert_image(self, rows, columns, r, g, b):
        image = np.random.randint(0, 65536, (rows, columns)).astype(np.uint16)
        h = color.Color(r, g, b)
        color_image = h.convert(image)
        assert color_image.shape == (rows, columns, 3)
        assert color_image.dtype == np.uint8
