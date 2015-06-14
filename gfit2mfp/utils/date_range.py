import datetime

class DateRange(object):
    def __init__(self, start, end):
        assert start < end
        self._start, self._end = start, end

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def duration(self):
        return self.end - self.start

    def near(self, other):
        '''
        Similar to contains, but returns if they are within five minutes of each other
        '''
        # if they're actually intersecting then we can shortcut
        if other in self:
            return True
        else:
            start_diff = self.start - other.start
            end_diff = self.end - other.end

    def __contains__(self, other):
        '''
        `x in my_date_range` will return true if `x` intersects the date range. If x is a datetime
        object, then it simply checks if it is in the middle. If x is another DateRange it checks
        whether the two intersect. So say your ranges look like so:

        my_date_range:      |------------|
        x:          |-----------|
        y:              |-------------------|
        z:                       |----|

        All three x, y and z will return True.
        '''
        if isinstance(other, DateRange):
            return self.start <= other.end and other.start <= self.end
        elif isinstance(other, datetime.datetime):
            return self.start <= other <= self.end

    def __lt__(self, other):
        '''
        this is smaller than the other if its start time is earlier. if they're identical
        then it looks at the end times
        '''
        if self.start == other.start:
            return self.end < other.end
        else:
            return self.start < other.start

    def __hash__(self):
        return hash((self.start, self.end))

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __str__(self):
        # trim the microseconds from timedelta - no-one cares about those anyway!
        trimmed_duration = datetime.timedelta(seconds=int(self.duration.total_seconds()))
        return 'DateRange s={0} d={1}'.format(self.start, trimmed_duration)

    def __repr__(self):
        return 'DateRange(start={0}, end={1})'.format(repr(self.start), repr(self.end))
