import json

from DataGenerator import *
from MyAlg import *
from TORA import *
from tqdm import tqdm
from ClosestDriver import *

import numpy as np


# set_of_values = [int(v) for v in np.arange(60, 430, 30)] # original
# set_of_values = [120]
set_of_values = [int(v) for v in np.arange(60, 310, 30)] # TEXAS

# interval_time = timedelta(seconds=300)
data_generator = DataGenerator()


# #austin
# number_of_requests = 5000
# number_of_drivers = 50
# request_intervals = 30
# avg_trip_distance = 6
# lat_range = [30, 31] #austin
# long_range = [-98, -97] #austin
# avg_speed = 40 / 3600  # 35 km/h #austin
# unit_emission_range = [70, 300]
# driver_move_range = [0.02, 0.02]
# unassigned_tol = 20



#Texas
# number_of_requests = 5000
number_of_drivers = 500
request_intervals = 30
avg_trip_distance = 6
lat_range = [41, 43]
long_range = [-86, -88]
avg_speed = 40 / 3600  # 35 km/h
unit_emission_range = [70, 300]
driver_move_range = [0.02, 0.02]
unassigned_tol = 20


# fixedLimit_10 = FixedLimit_Alg(driver_move_range=driver_move_range, distance_limit=10)
# fixedLimit_20 = FixedLimit_Alg(driver_move_range=driver_move_range, distance_limit=20)
# fixedLimit_30 = FixedLimit_Alg(driver_move_range=driver_move_range, distance_limit=30)
distance_options = [2, 5, 10, 15, 20, 25, 30]
alpha = 0.8
max_waiting_list = 100
V_coeff = 1
myAlg25 = MyAlg(driver_move_range=driver_move_range, distance_options=distance_options,
              max_waiting_list=max_waiting_list, alpha=0.25, V_coeff=V_coeff, lr=0.1)
myAlg5 = MyAlg(driver_move_range=driver_move_range, distance_options=distance_options,
              max_waiting_list=max_waiting_list, alpha=0.5, V_coeff=V_coeff, lr=0.1)
myAlg75 = MyAlg(driver_move_range=driver_move_range, distance_options=distance_options,
              max_waiting_list=max_waiting_list, alpha=0.8, V_coeff=V_coeff, lr=0.1)


tora = TORA(threshold=1, base_ev_emission=70, driver_move_range=driver_move_range)
closest = ClosestDriver(driver_move_range=driver_move_range)

algorithms = {}
algorithms['MyAlg-0.25'] = myAlg25
algorithms['MyAlg-0.50'] = myAlg5
algorithms['MyAlg-0.75'] = myAlg75
algorithms['TORA'] = tora
algorithms['CD'] = closest
# algorithms['Fixed-10'] = fixedLimit_10
# algorithms['Fixed-20'] = fixedLimit_20
# algorithms['Fixed-30'] = fixedLimit_30

trials = 1 # 10 for original


for alg_name in algorithms:
    algorithm = algorithms[alg_name]
    algorithm.reset()
    algorithm_result = {}
    ride_infos = {}
    driver_infos = {}

    for interval_time in set_of_values:
        algorithm_result[interval_time] = []
        ride_infos[interval_time] = []
        driver_infos[interval_time] = []
        for trial in range(trials):
            data_generator.reset()
            # data_generator.generate_synthetic_dataset(number_of_requests, number_of_drivers, request_intervals,
            #                                           avg_trip_distance,
            #                                           lat_range, long_range, unit_emission_range, avg_speed,
            #                                           unassigned_tol=unassigned_tol, dist_of_unit_emission='exp',
            #                                           random_gen_version=0)
            """
            Austin dataset
            """
            # data_path = "Data/merged_datasetAB_finaldatetime.csv" #Austin
            # request_periods = [pd.Timestamp('2016-12-1'), pd.Timestamp('2016-12-2')]
            #
            #
            # data_generator.read_dataset(data_path, number_of_drivers, avg_speed, unassigned_tol, lat_range, long_range,
            #                             request_periods,
            #                             avg_trip_distance, unit_emission_range=None, update_all=True)

            """
            Texas dataset
            """
            data_path = "Data/texas_Oct_2024_merged.csv"  # Texas
            request_periods = [pd.Timestamp('2025-10-1'), pd.Timestamp('2025-10-3')]
            data_generator.read_texas_dataset(data_path, number_of_drivers, avg_speed, unassigned_tol, lat_range, long_range,
                                        request_periods,
                                        avg_trip_distance, unit_emission_range=None, update_all=True)

            n_requests = len(data_generator.requests)

            print(
                f"\nAlg: {alg_name}- Parameter: {interval_time} - Trial: {trial+1} / {trials} - Dataset with {n_requests} requests and {len(data_generator.drivers)} drivers has been loaded.")
            with tqdm(total=len(data_generator.requests)) as pbar:
                batch_index = 0
                unassigned_traces = []
                while True:
                    requests, drivers, time = data_generator.next_batch(interval_time=timedelta(seconds=interval_time))
                    unassigned_traces.append(len(requests))
                    if len(requests) == 0:
                        break
                    if len(drivers) == 0:
                        for request in requests:
                            data_generator.add_to_queue(request)
                        continue

                    # print(
                    # f"{batch_index}) Evaluating batch with {len(requests)} requests and {len(drivers)} drivers at {time}")
                    batch_index += 1
                    params = {'update': True}  # parameter of myAlg
                    params['n_assigning'] = min(len(requests), len(drivers))
                    params['n_unassigned'] = len(requests)

                    for request in requests:
                        driver = algorithm.findDriver(request, drivers, time,closest_at_end=True, params=params)
                        if driver is not None:
                            # print(f"Request id: {request.ride_request_id} assigned to driver {driver.driver_id}")
                            algorithm.finalize_match(request, driver, time)
                            drivers.remove(driver)
                            pbar.update(1)
                        else:
                            data_generator.add_to_queue(request)

            requests = data_generator.get_all_requests()
            drivers = data_generator.get_all_drivers()

            start_time = requests[0].created_request_time
            serving_time = time - start_time

            total_emission = 0
            total_waiting = 0
            total_deadhead_distance = []
            total_trip_distance = []
            unassigned_requests = 0

            ride_driver_emissions = []
            ride_distances = []

            for driver in drivers:
                ride_driver_emissions.append((float(driver.unit_emission), len(driver.matched_requests)))

                for i in range(len(driver.trip_distances)):
                    ride_distances.append((float(driver.unit_emission), driver.deadhead_distances[i] / driver.trip_distances[i]))


            for request in requests:
                if request.matched_driver is None:
                    unassigned_requests += 1
                else:
                    total_emission += float(request.emission)
                    total_waiting += request.waiting_time
                    total_deadhead_distance.append(request.deadhead_distance)
                    if request.deadhead_distance > 30:
                        pass
                    total_trip_distance.append(request.trip_distance)

            if len(total_trip_distance) == 0:
                total_trip_distance = [-1]
            if len(total_deadhead_distance) == 0:
                total_deadhead_distance = [-1]
            total_info = {
                'avg_emission': total_emission / (data_generator.number_of_requests - unassigned_requests),
                'avg_waiting': total_waiting / (data_generator.number_of_requests - unassigned_requests),
                'avg_deadhead': float(np.average(total_deadhead_distance)),
                'min_deadhead': float(np.min(total_deadhead_distance)),
                'max_deadhead': float(np.max(total_deadhead_distance)),
                'avg_tripdistance': float(np.average(total_trip_distance)),
                'n_requests': data_generator.number_of_requests,
                'n_unassignment': unassigned_requests,
                'serving_time': serving_time.total_seconds(),
                'avg_req_intervals': data_generator.avg_intervals,
                'unassigned_traces': unassigned_traces}

            algorithm_result[interval_time].append(total_info)
            ride_infos[interval_time].append(ride_driver_emissions)


            driver_infos[interval_time].append(ride_distances)

    with open('results/Dataset_batchDuration/Texas_{0}.json'.format(alg_name), 'w') as writer:
        json.dump(algorithm_result, writer)

    with open('results/Dataset_batchDuration/rideInfo_Texas_{0}.json'.format(alg_name), 'w') as writer:
        json.dump(ride_infos, writer)

    with open('results/Dataset_batchDuration/driverInfo_Texas_{0}.json'.format(alg_name), 'w') as writer:
        json.dump(driver_infos, writer)


