import logging

from gfit2mfp import data_collection
from gfit2mfp import data_manipulation
from gfit2mfp import last_run
from gfit2mfp import mfp_upload
from gfit2mfp import settings

logging.basicConfig(
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)

start_time = last_run.update_last_run()

gfit = data_collection.GFitAPI(

    
)
with gfit:
    cal_data = gfit.get_cal_data()
    act_data = gfit.get_activity_data()

useful_stats = data_manipulation.summarise(cal_data)
print(useful_stats)

fitness_data = data_manipulation.combine_activities(cal_data, act_data)

day_data = data_manipulation.get_daily_summary(fitness_data)

# with mfp_upload.MFP(settings.MFP_USERNAME, settings.MFP_PASSWORD) as mfp:
#     mfp.upload(day_data)
