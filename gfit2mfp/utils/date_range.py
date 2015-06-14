import datetime

class DateRange(object):
    def __init__(self, start, end):
        self.start, self.end = start, end

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
            return other.start <= self.end or self.start <= other.end
        elif isinstance(other, datetime.datetime):
            return self.start <= other <= self.end

    def __repr__(self):
        return 'DateRange(start={0}, end={1})'.format(repr(self.start), repr(self.end))
