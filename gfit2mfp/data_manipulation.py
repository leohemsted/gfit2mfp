import logging
from operator import itemgetter
from datetime import timedelta

from gfit2mfp.utils import DateRange
from gfit2mfp.utils import Activity

logger = logging.getLogger(__name__)

def summarise(fit_data):
    '''
    Returns a dictionary containing some information summarising the entire period accounted for
    '''
    exercise_time = sum((d['times'].duration for d in fit_data['data']), timedelta())
    cals = sum(d['value'] for d in fit_data['data'])

    period = fit_data['times']

    return {
        'start': period.start,
        'end': period.end,
        'period_length': period.duration,

        'total_exercise_time': exercise_time,
        'total_cals': cals,

        'cals_per_day': cals / period.duration.days,
        'exercise_time_per_day': exercise_time / period.duration.days
    }


def combine_activities(cal_data, act_data):
    '''
    Returns a single dictionary of data points that were present in both cal and activity data
    '''
    cal_data = {d['times']: d['value'] for d in cal_data['data']}
    act_data = {d['times']: d['value'] for d in act_data['data']}
    cal_times = set(cal_data.keys())
    act_times = set(act_data.keys())
    intersect = cal_times & act_times
    inverse = cal_times ^ act_times


    # check that we didn't have too many unmatched items (10% of total count)
    if len(inverse) > 0.1 * len(cal_times):
        logger.warning(
            'Large amount of non-matching calorie and activity data (%i items)',
            len(inverse)
        )

    data = {
        time: {'cals': cal_data[time], 'activity': Activity(act_data[time])}
        for time in intersect if Activity(act_data[time]).valid()
    }

    return data

def merge_data(a, b):
    return {
        'times': a['times'].combine(b['times']),
        'cals': a['cals'] + b['cals'],
        'activity': a['activity']
    }


# def get_discrete_sessions(fit_data):
#     '''
#     Returns a dictionary of times with discrete sessions. If two data points have start and end
#     times that overlap, this combines them
#     '''
#     exercise_sessions = {}

#     for data in fit_data['data']:
#         data_key = data['times']
#         #
#         for group in exercise_sessions.keys():
#             if data_key in group:
#                 if exercise['activity'] != data['activity']:
#                     logger.warning(exercise[])
#                 else
#                     logger.debug('data intersects: %s in %s', data_key, group)
#                     # remove old one from list and combine with the new data point
#                     existing_data = exercise_sessions.pop(group)

#                     data = merge_data(existing_data, data)
#                     data_key = data['times']
#                     break

#         exercise_sessions[data_key] = data

#     logger.info(
#         'Compressed data down from %i to %i data points',
#         len(fit_data['data']),
#         len(exercise_sessions)
#     )

#     # make sure we didn't miss any rows
#     assert sum(x['value'] for x in fit_data['data']) == \
#         sum(x['value'] for x in exercise_sessions.values())

#     # sort by start date and return
#     return exercise_sessions
