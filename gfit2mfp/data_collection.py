import httplib2
import argparse
from datetime import datetime, timedelta

from googleapiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools

from gfit2mfp import settings
from gfit2mfp.utils import DateRange

API_SCOPE = 'https://www.googleapis.com/auth/fitness.activity.read'


def login():
    storage = Storage('user_credentials')
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        flow = OAuth2WebServerFlow(
            settings.CLIENT_ID,
            settings.CLIENT_SECRET,
            API_SCOPE
        )
        # google requires me to give an argparser for flags, although I know i'll be passing none in
        parser = argparse.ArgumentParser(parents=[tools.argparser])
        flags = parser.parse_args()
        credentials = tools.run_flow(flow, storage, flags)

    http = credentials.authorize(httplib2.Http())
    api = build('fitness', 'v1', http=http)
    return api


def get_time_range_str(start, end):
    # google accepts timestamps in nanoseconds
    start = int(start.timestamp() * 1e9)
    end = int(end.timestamp() * 1e9)
    return '{s}-{e}'.format(s=start, e=end)


def _get_fit_data(api, data_source, data_type):
    end = datetime.now()
    start = end - timedelta(days=5)

    response = api.users().dataSources().datasets().get(
        userId='me',
        dataSourceId=data_source,
        datasetId=get_time_range_str(start, end)
    ).execute()

    return preprocess_data(response, data_type)


def get_cal_data(api):
    data = 'derived:com.google.calories.expended:com.google.android.gms:from_activities'
    return _get_fit_data(api, data_source=data, data_type='fpVal')


def get_activity_data(api):
    data = 'derived:com.google.activity.segment:com.google.android.gms:merge_activity_segments'
    return _get_fit_data(api, data_source=data, data_type='intVal')


def process_datapoint(point, data_type):
    # no idea what might trip this one up
    if len(point['value']) != 1:
        print(point)
        raise NotImplementedError('can only handle one value in a point')

    start_ns = float(point['startTimeNanos'])
    end_ns = float(point['endTimeNanos'])

    start = datetime.fromtimestamp(start_ns / 1e9)
    end = datetime.fromtimestamp(end_ns / 1e9)

    # the calories burnt between start and end
    return {
        'times': DateRange(start, end),
        'value': point['value'][0][data_type]
    }


def preprocess_data(data, data_type):
    global_start = datetime.fromtimestamp(float(data['minStartTimeNs'])/1e9)
    global_end = datetime.fromtimestamp(float(data['maxEndTimeNs'])/1e9)
    return {
        'times': DateRange(global_start, global_end),
        'data': [process_datapoint(point, data_type) for point in data['point']]
    }
