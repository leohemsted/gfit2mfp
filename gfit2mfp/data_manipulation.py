import logging
from operator import itemgetter
from datetime import timedelta

from gfit2mfp.utils import DateRange

logger = logging.getLogger(__name__)

def summarise(fit_data):
    '''
    Returns a dictionary containing some information summarising the entire period accounted for
    '''
    excercise_time = sum((d['times'].duration for d in fit_data['data']), timedelta())
    cals = sum(d['value'] for d in fit_data['data'])

    period = fit_data['times']

    return {
        'start': period.start,
        'end': period.end,
        'period_length': period.duration,

        'total_excercise_time': excercise_time,
        'total_cals': cals,

        'cals_per_day': cals / period.duration.days,
        'excercise_time_per_day': excercise_time / period.duration.days
    }


def merge_data(a, b):
    return {
        'times': a['times'].combine(b['times']),
        'value': a['value'] + b['value']
    }


def get_discrete_sessions(fit_data):
    '''
    Returns a list of discrete sessions. If two data points have start and end times that overlap,
    this combines them
    '''
    excercise_groups = {}

    for data in fit_data['data']:
        data_key = data['times']
        #
        for group in excercise_groups.keys():
            if data_key in group:
                logger.debug('data intersects: %s in %s', data_key, group)
                # remove old one from list and combine with the new data point
                existing_data = excercise_groups.pop(group)
                data = merge_data(existing_data, data)
                data_key = data['times']
                break

        excercise_groups[data_key] = data

    logger.info(
        'Compressed data down from %i to %i data points',
        len(fit_data['data']),
        len(excercise_groups)
    )

    # make sure we didn't miss any rows
    assert sum(x['value'] for x in fit_data['data']) == \
        sum(x['value'] for x in excercise_groups.values())

    # sort by start date and return
    return sorted(
        excercise_groups.values(),
        key=itemgetter('times')
    )
