from gfit2mfp import data_collection, data_manipulation

api = data_collection.login()
fit_data = data_collection.get_fit_data(api)
useful_stats = data_manipulation.summarise(fit_data)
import pdb
pdb.set_trace()
