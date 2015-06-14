from datetime import datetime as dt

import pytest

try:
    from unittest.mock import Mock
except ImportError:
    # python 2.x compatibility
    from mock import Mock

from gfit2mfp.utils import DateRange


def test_create_date_range():
    s = Mock()
    e = Mock()
    obj = DateRange(s, e)

    assert obj.start == s
    assert obj.end == e

@pytest.mark.parametrize('start, end, other_start, other_end',
    # just use ints in this test because writing datetimes is hard work
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
    ]
)
def test_compare_date_ranges_intersect(start, end, other_start, other_end):
    obj = DateRange(start, end)
    other = DateRange(other_start, other_end)

    assert other in obj



@pytest.mark.parametrize('start, end, other',
    [
        # date is before
        pytest.mark.xfail((dt(2000, 1, 5), dt(2000, 1, 10), dt(2000, 1, 1))),
        # date is exactly equal to start
        (dt(2000, 1, 5), dt(2000, 1, 10), dt(2000, 1, 5)),
        # date is in the middle
        (dt(2000, 1, 5), dt(2000, 1, 10), dt(2000, 1, 7)),
        # date is exactly equal to end
        (dt(2000, 1, 5), dt(2000, 1, 10), dt(2000, 1, 10)),
        # date is after
        pytest.mark.xfail((dt(2000, 1, 5), dt(2000, 1, 10), dt(2000, 1, 12)))
    ]
)
def test_compare_date_ranges_contains_date(start, end, other):
    obj = DateRange(start, end)

    assert other in obj
