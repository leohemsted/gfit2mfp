import datetime

class DateRange(object):
    def __init__(self, start, end):
        self.start, self.end = start, end

    def __contains__(self, other):
        if isinstance(other, DateRange):
            return other.start <= self.end or self.start <= other.end
        elif isinstance(other, datetime.datetime):
            return self.start < other <= self.end

    def __repr__(self):
        return 'DateRange(start={0}, end={1})'.format(repr(self.start), repr(self.end))
