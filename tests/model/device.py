import unittest
import hypothesis.strategies as st
from hypothesis import given
from fylm.model.device import Device


class DeviceTests(unittest.TestCase):
    @given(st.integers())
    def test_enums_work(self, number):
        assert Device.original != number
        assert Device.plinko != number
        assert Device.cerevisiae != number

    def test_device_unique(self):
        # Ensures I understood the enum documentation correctly
        devices = [d for d in Device]
        matches = [d1 == d2 for d1 in Device for d2 in Device]
        self.assertEqual(len(list(filter(None, matches))), len(devices))
