from DataGenerator import *
from FixedLimit_Alg import *
import json
from datetime import datetime, timedelta
import numpy as np
from TORA import *

# from tqdm import tqdm

interval_time = timedelta(seconds=300)
distance_limit = 200  # km
data_generator = DataGenerator()  # TODO

number_of_requests = 5000
number_of_drivers = 250
request_intervals = 30
avg_trip_distance = 15
lat_range = [30, 31]
long_range = [-98, -97]
unit_emission_range = [70, 300]
avg_speed = 40 / 3600  # 35 km/h
driver_move_range = [0.01, 0.01]
data_generator.generate_synthetic_dataset(number_of_requests, number_of_drivers, request_intervals, avg_trip_distance,
                                          lat_range, long_range, unit_emission_range, avg_speed,
                                          dist_of_unit_emission='exp')

# algorithm = FixedLimit_Alg(driver_move_range= driver_move_range, distance_limit=distance_limit)
algorithm = TORA(threshold=1, base_ev_emission=63.35, driver_move_range=driver_move_range)
batch_index = 0
while True:
    requests, drivers, time = data_generator.next_batch(interval_time=interval_time)
    if len(requests) == 0:
        break
    if len(drivers) == 0:
        continue

    print(f"{batch_index}) Evaluating batch with {len(requests)} requests and {len(drivers)} drivers at {time}")
    batch_index += 1

    for request in requests:
        driver = algorithm.findDriver(request, drivers, time)
        if driver is not None:
            # print(f"Request id: {request.ride_request_id} assigned to driver {driver.driver_id}")
            algorithm.finalize_match(request, driver, time)
            drivers.remove(driver)
            data_generator.next()

requests = data_generator.get_all_requests()
drivers = data_generator.get_all_drivers()

start_time = requests[0].created_request_time
serving_time = time - start_time

total_emission = 0
total_waiting = 0
total_deadhead_distance = []
total_trip_distance = []

request_dataset = []
for request in requests:
    request_data = {
        'ride_request_id': request.ride_request_id,
        'matched_driver_id': request.matched_driver,
        'waiting_times': request.waiting_time,
        'trip_distance': request.trip_distance,
        'deadhead_distance': request.deadhead_distance,
        'emission': float(request.emission)
    }
    total_emission += float(request.emission)
    total_waiting += request.waiting_time
    total_deadhead_distance.append(request.deadhead_distance)
    total_trip_distance.append(request.trip_distance)
    request_dataset.append(request_data)

with open('results/test/TORAtotal.json', 'w') as writer:
    total_info = {
        'avg_emission': total_emission / number_of_requests,
        'avg_waiting': total_waiting / number_of_requests,
        'avg_deadhead': float(np.average(total_deadhead_distance)),
        'min_deadhead': float(np.min(total_deadhead_distance)),
        'max_deadhead': float(np.max(total_deadhead_distance)),
        'avg_tripdistance': float(np.average(total_trip_distance)),
        'n_requests': number_of_requests,
        'serving_time': serving_time.seconds

    }
    json.dump(total_info, writer)

with open("results/test/TORArequests.json", 'w') as writer:
    json.dump(request_dataset, writer)

driver_dataset = []
for driver in drivers:
    driver_data = {
        'driver_id': int(driver.driver_id),
        'unit_emission': float(driver.unit_emission),
        'trip_distances': driver.trip_distances,
        'deadhead_distances': driver.deadhead_distances,
        'matched_requests': driver.matched_requests
    }
    driver_dataset.append(driver_data)

with open("results/test/TORAdrivers.json", 'w') as writer:
    json.dump(driver_dataset, writer)
