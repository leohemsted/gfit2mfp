import logging

from gfit2mfp import data_collection
from gfit2mfp import data_manipulation
from gfit2mfp import last_run
from gfit2mfp import settings

logging.basicConfig(
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)

start_time = last_run.retrieve_last_run()

gfit = data_collection.GfitAPI(
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    start=start_time
)
with gfit:
    cal_data = gfit.get_cal_data()
    act_data = gfit.get_activity_data()

useful_stats = data_manipulation.summarise(cal_data)
print(useful_stats)

fitness_data = data_manipulation.combine_activities(cal_data, act_data)

day_data = data_manipulation.get_daily_summary(fitness_data)

last_run.update_last_run()

# with mfp_upload.MFP(settings.MFP_USERNAME, settings.MFP_PASSWORD) as mfp:
#     mfp.upload(day_data)
