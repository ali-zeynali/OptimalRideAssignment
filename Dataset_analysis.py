import json

from DataGenerator import *
# from MyAlg import *
# from Synthetic_alg_params import avg_trip_distance
# from TORA import *
# from tqdm import tqdm
# from ClosestDriver import *

import numpy as np


# data_path = "Data/merged_datasetAB_finaldatetime.csv" #Austin
data_path = "Data/texas_Oct_2024_merged.csv" #Texas
request_periods = [pd.Timestamp('2025-10-1'), pd.Timestamp('2025-10-7')]
data_generator = DataGenerator()

number_of_drivers = 1
avg_speed = 1
unassigned_tol = 1
lat_range = [0, 90]
long_range = [-200, 200]
avg_trip_distance = 10
# data_generator.read_dataset(data_path, number_of_drivers, avg_speed, unassigned_tol, lat_range, long_range,
#                             request_periods,
#                             avg_trip_distance, unit_emission_range=None, update_all=True)

data_generator.read_texas_dataset(data_path, number_of_drivers, avg_speed, unassigned_tol, lat_range, long_range,
                            request_periods,
                            avg_trip_distance, unit_emission_range=None, update_all=True)

prev_time = None
diffs = []
max_diff = 600
for request in data_generator.requests:
    req_time = request.created_request_time
    if prev_time is not None:
        diff = (req_time - prev_time).total_seconds()
        if diff < max_diff:
            diffs.append(diff)

    prev_time = req_time

print(np.mean(diffs))
print(len(data_generator.requests))




