from datetime import datetime, timedelta

import httplib2

from googleapiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

from . import settings

FIT_URL_STRING = 'https://www.googleapis.com/fitness/v1/users/{userId}/dataSources/{dataSourceId}/datasets/{datasetId}'
DEV_ID = 'me'

def login():
    storage = Storage('user_credentials')
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        flow = OAuth2WebServerFlow(
            settings.CLIENT_ID,
            settings.CLIENT_SECRET,
            settings.API_SCOPE
        )
        credentials = run(flow, storage)

    http = credentials.authorize(httplib2.Http())
    api = build('fitness', 'v1', http=http)
    return api

def get_time_range_str(start, end):
    # google accepts timestamps in nanoseconds
    start = int(start.timestamp() * 1e9)
    end = int(end.timestamp() * 1e9)
    return '{s}-{e}'.format(s=start, e=end)

def get_fit_data():
    end = datetime.now()
    start = end - timedelta(days=5)
    url = FIT_URL_STRING.format(
        userId='me',
        dataSourceId='derived:com.google.calories.expended:com.google.android.gms:from_activities',
        datasetId=get_time_range_str(start, end)
    )
    request = api.users(userId='me').dataSources().list()

    while request is not None:
        response = request.execute()
        import pdb
        pdb.set_trace()

if __name__ == '__main__':
    api = login()
    get_fit_data(api)
