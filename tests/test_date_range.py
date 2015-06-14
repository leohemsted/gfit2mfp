from datetime import datetime as dt, date as d, time as t

import pytest

from gfit2mfp.utils import DateRange


def test_create_date_range():
    obj = DateRange(1, 2)

    assert obj.start == 1
    assert obj.end == 2


@pytest.mark.parametrize(
    'start, end, other_start, other_end',
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
        (2, 4, 4, 5)
    ]
)
def test_date_ranges_intersect(start, end, other_start, other_end):
    obj = DateRange(start, end)
    other = DateRange(other_start, other_end)

    assert other in obj


@pytest.mark.parametrize(
    'start, end, other_start, other_end',
    [
        # other range starts after
        (2, 4, 5, 6),
        # other range ends before
        (2, 4, 0, 1)
    ]
)
def test_date_ranges_dont_intersect(start, end, other_start, other_end):
    obj = DateRange(start, end)
    other = DateRange(other_start, other_end)

    assert other not in obj


@pytest.mark.parametrize(
    'start, end, other',
    [
        # date is exactly equal to start
        (dt(2000, 1, 5), dt(2000, 1, 10), dt(2000, 1, 5)),
        # date is in the middle
        (dt(2000, 1, 5), dt(2000, 1, 10), dt(2000, 1, 7)),
        # date is exactly equal to end
        (dt(2000, 1, 5), dt(2000, 1, 10), dt(2000, 1, 10)),
    ]
)
def test_date_ranges_contains_date(start, end, other):
    obj = DateRange(start, end)

    assert other in obj
    assert obj.near(other)

@pytest.mark.parametrize(
    'start, end, other',
    [
        # date is before
        (dt(2000, 1, 5), dt(2000, 1, 10), dt(2000, 1, 1)),
        # date is after
        (dt(2000, 1, 5), dt(2000, 1, 10), dt(2000, 1, 12))
    ]
)
def test_date_ranges_not_contains_date(start, end, other):
    obj = DateRange(start, end)

    assert other not in obj

def test_date_ranges_equal():
    obj = DateRange(dt(2000, 1, 5), dt(2000, 1, 10))
    other = DateRange(dt(2000, 1, 5), dt(2000, 1, 10))

    assert obj == other

def test_hash_is_consistent():
    obj = DateRange(dt(2000, 1, 5), dt(2000, 1, 10))
    other = DateRange(dt(2000, 1, 5), dt(2000, 1, 10))

    assert hash(obj) == hash(other)

@pytest.mark.parametrize(
    'start, end, other_start, other_end',
    [
        # the other date range just clips the start
        (t(12, 10, 0), t(13, 10, 0), t(12, 0, 0), t(12, 5, 0)),
        # the other date range just clips the end
        (t(12, 10, 0), t(13, 10, 0), t(13, 15, 0), t(13, 20, 0)),
    ]
)
def test_date_ranges_near(start, end, other_start, other_end):
    date = d(2000, 1, 5)
    obj = DateRange(dt.combine(date, start), dt.combine(date, end))
    other = DateRange(dt.combine(date, other_start), dt.combine(date, other_end))

    assert obj.near(other)

@pytest.mark.parametrize(
    'start, end, other_start, other_end',
    [
        # the other date range just misses the start
        (t(12, 10, 0), t(13, 10, 0), t(12, 0, 0), t(12, 4, 59)),
        # the other date range just misses the end
        (t(12, 10, 0), t(13, 10, 0), t(13, 15, 1), t(13, 20, 0))
    ]
)
def test_date_ranges_arent_near(start, end, other_start, other_end):
    date = d(2000, 1, 5)
    obj = DateRange(dt.combine(date, start), dt.combine(date, end))
    other = DateRange(dt.combine(date, other_start), dt.combine(date, other_end))

    assert not obj.near(other)


@pytest.mark.parametrize(
    'start, end, other',
    [
        # the other date range just clips the start
        (t(12, 10, 0), t(13, 10, 0), t(12, 5, 0)),
        # the other date range just clips the end
        (t(12, 10, 0), t(13, 10, 0), t(13, 15, 0))
    ]
)
def test_date_ranges_near_date(start, end, other):
    date = d(2000, 1, 5)
    obj = DateRange(dt.combine(date, start), dt.combine(date, end))

    assert obj.near(dt.combine(date, other))

@pytest.mark.parametrize(
    'start, end, other',
    [
        # the other date range just misses the start
        (t(12, 10, 0), t(13, 10, 0), t(12, 4, 59)),
        # the other date range just misses the end
        (t(12, 10, 0), t(13, 10, 0), t(13, 15, 1)),
    ]
)
def test_date_ranges_not_near_date(start, end, other):
    date = d(2000, 1, 5)
    obj = DateRange(dt.combine(date, start), dt.combine(date, end))

    assert not obj.near(dt.combine(date, other))

