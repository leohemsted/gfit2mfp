import logging
from datetime import timedelta

from gfit2mfp.utils import DateRange

logger = logging.getLogger(__name__)

def summarise(fit_data):
    '''
    Returns a dictionary containing some information summarising the entire period accounted for
    '''
    excercise_time = sum((d['end'] - d['start'] for d in fit_data['data']), timedelta())
    cals = sum(d['cals'] for d in fit_data['data'])
    period = fit_data['end'] - fit_data['start']

    return {
        'start': fit_data['start'],
        'end': fit_data['end'],
        'period_length': period,

        'total_excercise_time': excercise_time,
        'total_cals': cals,

        'cals_per_day': cals / period.days,
        'excercise_time_per_day': excercise_time / period.days
    }


def merge_data(a, b):
    return {
        'start': min(a['start'], b['start']),
        'end': max(a['end'], b['end']),
        'cals': a['cals'] + b['cals']
    }


def get_discrete_sessions(fit_data):
    '''
    Returns a list of discrete sessions. If two data points have start and end times that overlap,
    this combines them
    '''
    excercise_groups = {}

    for data in fit_data['data']:
        data_key = DateRange(data['start'], data['end'])
        #
        for group in excercise_groups.keys():
            if data_key in group:
                logger.debug('data intersects: %s in %s', data_key, group)
                # remove old one from list and combine with the new data point
                existing_data = excercise_groups.pop(group)
                data = merge_data(existing_data, data)
                data_key = DateRange(data['start'], data['end'])
                break

        excercise_groups[data_key] = data

    logger.info(
        'Compressed data down from %i to %i data points',
        len(fit_data['data']),
        len(excercise_groups)
    )

    # make sure we didn't miss any rows
    assert sum(x['cals'] for x in fit_data['data']) == \
        sum(x['cals'] for x in excercise_groups.values())

    # sort by start date and return
    return sorted(excercise_groups.values(), key=lambda x: DateRange(x['start'], x['end']))
