import itertools
from datetime import timedelta


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


def get_discrete_sessions(fit_data):
    '''
    Returns a list of discrete sessions. If two data points have start and end times that overlap or
    are within a minute of each other, this combines them
    '''

    excercise_groups = {}

    for data in fit_data:
        data_key = DateRange(data['start'], data['end'])
        excercise_groups.keys()
        import pdb
        pdb.set_trace()


