import logging
import re
import requests

logger = logging.getLogger(__name__)

class MFP(object):
    login_url = 'https://www.myfitnesspal.com/account/login'
    add_exercise_url = 'http://www.myfitnesspal.com/exercise/add'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.csrf = None
        self.client = None
        super().__init__()

    def __enter__(self):
        self.client = requests.session()
        self.authenticate()
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if self.client:
            self.client.close()

    def authenticate(self):
        # Retrieve the CSRF token first
        login_page = self.client.get(self.login_url)

        self.csrf = re.search(r'<meta content="(.*)" name="csrf-token" />', login_page.text).group(1)

        logger.info('Logging in with csrf token %s', self.csrf)

        ret = self.client.post(
            self.login_url,
            headers={'Referer': self.login_url},
            data={
                'username': self.username,
                'password': self.password,
                'authenticity_token': self.csrf,
                'utf8': '✓'
            }
        )
        logger.info('Login: %s', ret)

    def upload(self, days):
        for day, activities in days.items():
            for activity, data in activities.items():
                self.enter_activity(activity, day, data['cals'], data['duration'])

    def enter_activity(self, activity, date, cals, duration):
        payload = {
            'utf8':'✓',
            'authenticity_token':self.csrf,
            'calorie_multiplier':1.0,
            'search':activity.name,
            'exercise_entry[exercise_id]':activity.mfp_id,
            'exercise_entry[date]':str(date),
            # todo: figure out what this represents
            'exercise_entry[exercise_type]':0,
            'exercise_entry[quantity]':duration.seconds / 60,
            'exercise_entry[calories]':cals,
        }
        logging.info(
            'Sending activity data: %s, %s, %i cals, %i mins',
            activity,
            date,
            cals,
            duration.seconds / 60
        )
        res = self.client.post(self.add_exercise_url, data=payload)
        import pdb; pdb.set_trace()

        if re.search('Please correct the following errors', res.text):
            with open('error.html', 'w', encoding='utf-8') as err:
                err.write(res.text)
            raise ValueError('MyFitnessPal did not return 302. Error page saved to \'error.html\'')
