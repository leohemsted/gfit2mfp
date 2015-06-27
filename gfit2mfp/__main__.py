import logging
import json
from os.path import isfile

logging.basicConfig(
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)

from gfit2mfp import data_collection, data_manipulation


# test file to save hitting google each time
cals = 'cal_data.json'
acts = 'activity_data.json'
if isfile(cals) and isfile(acts):
    with open(cals, 'r') as cal_file, open(acts, 'r') as act_file:
        cal_data = json.load(cal_file)
        act_data = json.load(act_file)

        cal_data = data_collection.preprocess_data(cal_data, 'fpVal')
        act_data = data_collection.preprocess_data(act_data, 'intVal')
else:
    api = data_collection.login()
    cal_data = data_collection.get_cal_data(api)
    act_data = data_collection.get_activity_data(api)

useful_stats = data_manipulation.summarise(cal_data)
print(useful_stats)
grouped_session = data_manipulation.get_discrete_sessions(cal_data)
print(grouped_session)
