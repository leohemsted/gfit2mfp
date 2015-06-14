import httplib2, argparse
from datetime import datetime, timedelta

from googleapiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools

from gfit2mfp import settings

API_SCOPE = 'https://www.googleapis.com/auth/fitness.activity.read'
FIT_URL_STRING = 'https://www.googleapis.com/fitness/v1/users/{userId}/dataSources/{dataSourceId}/datasets/{datasetId}'

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

def get_fit_data(api):
    end = datetime.now()
    start = end - timedelta(days=5)

    # api.users().dataSources().list(userId='me').execute()

    cal_datasource = 'derived:com.google.calories.expended:com.google.android.gms:from_activities'

    response = api.users().dataSources().datasets().get(
        userId='me',
        dataSourceId=cal_datasource,
        datasetId=get_time_range_str(start, end)
    ).execute()

    return preprocess_fit_data(response)

def process_fit_datapoint(point):
    # no idea what might trip this one up
    if len(point['value']) != 1:
        print(point)
        raise NotImplementedError('can only handle one calorie value in a point')

    start_ns = float(point['startTimeNanos'])
    end_ns = float(point['endTimeNanos'])

    start = datetime.fromtimestamp(start_ns / 1e9)
    end = datetime.fromtimestamp(end_ns / 1e9)

    # the calories burnt between start and end
    return {
        'start': start,
        'end': end,
        'cals': point['value'][0]['fpVal']
    }

def preprocess_fit_data(data):
    output_data = [process_fit_datapoint(point) for point in data['point']]

    global_start = datetime.fromtimestamp(float(data['minStartTimeNs'])/1e9)
    global_end = datetime.fromtimestamp(float(data['maxEndTimeNs'])/1e9)
    return {
        'start': global_start,
        'end': global_end,
        'data': output_data
    }
