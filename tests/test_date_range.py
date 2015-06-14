import unittest
from unittest.mock import Mock
from gfit2mfp.utils import DateRange

class TestDateRange(unittest.TestCase):
    def test_create_date_range(self):
        s = Mock()
        e = Mock()
        obj = DateRange(s, e)

        self.assertEqual(obj.start, s)
        self.assertEqual(obj.end, e)

