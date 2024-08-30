import json

from DataGenerator import *
from MyAlg import *
from TORA import *
from matplotlib import pyplot as plt
import pandas as pd
from FixedLimit_Alg import *
# from tqdm import tqdm

interval_time = timedelta(seconds=300)
distance_limit = 50  # km
data_generator = DataGenerator()  # TODO

number_of_requests = 5000
number_of_drivers = 120 #120 for synthetic
request_intervals = 30
avg_trip_distance = 15
lat_range = [30, 31]
long_range = [-98, -97]
unit_emission_range = [70, 300]
avg_speed = 40 / 3600  # 35 km/h
driver_move_range = [0.01, 0.01]
unassigned_tol = 10

# interval_time = timedelta(seconds=300)
# distance_limit = 50  # km
# data_generator = DataGenerator()
#
# number_of_requests = 5000
# number_of_drivers = 200
# request_intervals = 30
# avg_trip_distance = 15
# lat_range = [30, 31]
# long_range = [-98, -97]
# unit_emission_range = [70, 300]
# avg_speed = 40 / 3600  # 35 km/h
# driver_move_range = [0.01, 0.01]
# unassigned_tol = 10


data_generator.generate_synthetic_dataset(number_of_requests, number_of_drivers, request_intervals, avg_trip_distance,
                                          lat_range, long_range, unit_emission_range, avg_speed,
                                          unassigned_tol=unassigned_tol, dist_of_unit_emission='exp',
                                          random_gen_version=1)

# data_path = "Data/merged_datasetAB_finaldatetime.csv"
# request_periods = [pd.Timestamp('2016-12-1'), pd.Timestamp('2016-12-4')]
# data_generator.read_dataset(data_path, number_of_drivers, avg_speed, unassigned_tol, lat_range, long_range, request_periods,
#                      avg_trip_distance, unit_emission_range=unit_emission_range)

print(f"Dataset with {len(data_generator.requests)} requests and {len(data_generator.drivers)} drivers have been loaded.")


alg_name = 'TORA'


if alg_name == "FixedLIMIT":
    algorithm = FixedLimit_Alg(driver_move_range= driver_move_range, distance_limit=distance_limit)


distance_options = [1, 2, 5, 10, 15, 30]
gamma = 0.1
max_waiting_list = 20
V_coeff = 1
if alg_name == "MyAlg":
    algorithm = MyAlg(driver_move_range=driver_move_range, distance_options=distance_options,
                  max_waiting_list=max_waiting_list, gamma=gamma, V_coeff=V_coeff, lr=0.1)

if alg_name == "TORA":
    algorithm = TORA(threshold=1, base_ev_emission=70, driver_move_range=driver_move_range)
# initial_utilities = algorithm.utility_function.copy()

batch_index = 0
unassigned_traces = []
while True:
    requests, drivers, time = data_generator.next_batch(interval_time=interval_time)
    unassigned_traces.append(len(requests))
    if len(requests) == 0:
        break
    if len(drivers) == 0:
        for request in requests:
            data_generator.add_to_queue(request)
        continue

    print(f"{batch_index}) Evaluating batch with {len(requests)} requests and {len(drivers)} drivers at {time}")
    batch_index += 1
    params = {'update': True}  # parameter of myAlg
    params['n_assigning'] = min(len(requests), len(drivers))
    params['n_unassigned'] = len(requests)

    for request in requests:
        driver = algorithm.findDriver(request, drivers, time, params=params)
        if driver is not None:
            # print(f"Request id: {request.ride_request_id} assigned to driver {driver.driver_id}")
            algorithm.finalize_match(request, driver, time)
            drivers.remove(driver)
        else:
            data_generator.add_to_queue(request)

# print(f"Algorithm distance options: {algorithm.distance_options}")
# print(f"Initial Utilities: {initial_utilities}")
# print(f"Utilities: {algorithm.utility_function}")
# print(f"Avg calculated trip distance: {algorithm.d0}")
# exit(0)

requests = data_generator.get_all_requests()
drivers = data_generator.get_all_drivers()

start_time = requests[0].created_request_time
serving_time = time - start_time

total_emission = 0
total_waiting = 0
total_deadhead_distance = []
total_trip_distance = []
unassigned_requests = 0

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
    if request.matched_driver is None:
        unassigned_requests += 1
    else:
        total_emission += float(request.emission)
        total_waiting += request.waiting_time
        total_deadhead_distance.append(request.deadhead_distance)
        if request.deadhead_distance > 30:
            pass
        total_trip_distance.append(request.trip_distance)
        request_dataset.append(request_data)

with open('results/test/total.json', 'w') as writer:
    total_info = {
        'avg_emission': total_emission / data_generator.number_of_requests,
        'avg_waiting': total_waiting / data_generator.number_of_requests,
        'avg_deadhead': float(np.average(total_deadhead_distance)),
        'min_deadhead': float(np.min(total_deadhead_distance)),
        'max_deadhead': float(np.max(total_deadhead_distance)),
        'avg_tripdistance': float(np.average(total_trip_distance)),
        'n_requests': data_generator.number_of_requests,
        'n_unassignment': unassigned_requests,
        'serving_time': serving_time.seconds,
        'avg_req_intervals': data_generator.avg_intervals

    }
    json.dump(total_info, writer)

with open("results/test/requests.json", 'w') as writer:
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

with open("results/test/drivers.json", 'w') as writer:
    json.dump(driver_dataset, writer)


plt.plot(list(range(len(unassigned_traces)))[:-10], unassigned_traces[:-10])
plt.xlabel("Batch index")
plt.ylabel("# Unassigned requests")
plt.savefig("results/test/{0}.png".format(alg_name), dpi=300,  bbox_inches='tight')