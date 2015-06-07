from datetime import datetime, timedelta

import httplib2, argparse

from googleapiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools

from . import settings

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
