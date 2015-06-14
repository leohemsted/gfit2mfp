from datetime import datetime

import pytest
from unittest.mock import Mock

from gfit2mfp.utils import DateRange


def test_create_date_range():
    s = Mock()
    e = Mock()
    obj = DateRange(s, e)

    assert obj.start == s
    assert obj.end == e

@pytest.mark.parametrize('start, end, other_start, other_end',
    [
    # the other date range starts after, ends after
    (2, 4, 3, 5),
    # starts before, ends before
    (2, 4, 1, 3),
    # starts before, ends after
    (2, 4, 1, 5),
    # starts before, ends the exact same time as this one starts
    (2, 4, 1, 2),
    # starts exactly when this one ends, ends after
    (2, 4, 4, 5),

    # fail cases

    # other range starts after
    pytest.mark.xfail((2, 4, 5, 6)),
    # other range ends before
    pytest.mark.xfail((2, 4, 0, 1))
])
def test_compare_date_ranges_contained(start, end, other_start, other_end):
    obj = DateRange(start, end)
    other = DateRange(other_start, other_end)

    assert other in obj
