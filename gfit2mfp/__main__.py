import logging
import json
from os.path import isfile

from gfit2mfp import settings
from gfit2mfp import data_collection
from gfit2mfp import data_manipulation
from gfit2mfp import mfp_upload

logging.basicConfig(
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)

api = data_collection.login()
cal_data = data_collection.get_cal_data(api)
act_data = data_collection.get_activity_data(api)

useful_stats = data_manipulation.summarise(cal_data)
print(useful_stats)

fitness_data = data_manipulation.combine_activities(cal_data, act_data)

day_data = data_manipulation.get_daily_summary(fitness_data)

with mfp_upload.MFP(settings.MFP_USERNAME, settings.MFP_PASSWORD) as mfp:
    mfp.upload(day_data)
