import httplib2
import argparse
from datetime import datetime, timedelta

from googleapiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools

from gfit2mfp.utils import DateRange

API_SCOPE = 'https://www.googleapis.com/auth/fitness.activity.read'

class GfitAPI(object):
    def __init__(self, client_id, client_secret, start=None):
        if start is None:
            start = datetime.now() - timedelta(days=5)

        self.start = start
        self.api = None
        self.client_id = client_id
        self.client_secret = client_secret
        self.credentials = None
        super().__init__()

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        # not sure if I want to revoke - i might remove this later
        if self.credentials:
            self.credentials.revoke()

    def login(self):
        # code liberated from https://cloud.google.com/appengine/docs/python/endpoints/access_from_python
        storage = Storage('user_credentials')
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            flow = OAuth2WebServerFlow(
                self.client_id,
                self.client_secret,
                API_SCOPE
            )
            # google requires me to give an argparser for flags, although I know i'll be passing none in
            parser = argparse.ArgumentParser(parents=[tools.argparser])
            flags = parser.parse_args()
            self.credentials = tools.run_flow(flow, storage, flags)

        http = self.credentials.authorize(httplib2.Http())
        self.api = build('fitness', 'v1', http=http)


    def _get_fit_data(self, data_source, data_type):
        response = self.api.users().dataSources().datasets().get(
            userId='me',
            dataSourceId=data_source,
            datasetId=self.get_time_range_str(self.start, datetime.now())
        ).execute()

        return self.preprocess_data(response, data_type)


    def get_cal_data(self):
        data = 'derived:com.google.calories.expended:com.google.android.gms:from_activities'
        return self._get_fit_data(data_source=data, data_type='fpVal')


    def get_activity_data(self):
        data = 'derived:com.google.activity.segment:com.google.android.gms:merge_activity_segments'
        return self._get_fit_data(data_source=data, data_type='intVal')


    def process_datapoint(self, point, data_type):
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


    def preprocess_data(self, data, data_type):
        global_start = datetime.fromtimestamp(float(data['minStartTimeNs'])/1e9)
        global_end = datetime.fromtimestamp(float(data['maxEndTimeNs'])/1e9)
        return {
            'times': DateRange(global_start, global_end),
            'data': [self.process_datapoint(point, data_type) for point in data['point']]
        }
        

    @staticmethod
    def get_time_range_str(start, end):
    # google accepts timestamps in nanoseconds
    start = int(start.timestamp() * 1e9)
    end = int(end.timestamp() * 1e9)
    return '{s}-{e}'.format(s=start, e=end)
