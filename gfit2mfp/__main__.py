import json
import os.path

from gfit2mfp import data_collection, data_manipulation

# test file to save hitting google each time
fname = 'fit_data_test.json'
if os.path.isfile(fname):
    with open('fit_data_test.json', 'r') as json_data:
        raw_response = json.load(json_data)
        fit_data = data_collection.preprocess_fit_data(raw_response)
else:
    api = data_collection.login()
    fit_data = data_collection.get_fit_data(api)

useful_stats = data_manipulation.summarise(fit_data)
