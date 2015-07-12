import requests

class MFP(object):
    login_url = 'https://www.myfitnesspal.com/account/login'

    def __init__(self, username, password):
        super().__init__()

    def authenticate(self):
        client = requests.session()

        # Retrieve the CSRF token first
        client.get(self.login_url)
        import pdb; pdb.set_trace()

        csrftoken = client.cookies['csrf']

        login_data = dict(username=EMAIL, password=PASSWORD, csrfmiddlewaretoken=csrftoken, next='/')

        r = client.post(URL, data=login_data, headers=dict(Referer=URL))
        pass

    def upload(self, days):
        for day, activities in days.items():
            for activity, data in activities.items():
                self.enter_activity(activity, day, data['cals'], data['duration'])

    def enter_activity(self, activity, date, cals, duration):
        pass
