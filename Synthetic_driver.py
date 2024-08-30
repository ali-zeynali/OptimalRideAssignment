import json

from DataGenerator import *
from MyAlg import *
from TORA import *
# from matplotlib import pyplot as plt
# import pandas as pd
from FixedLimit_Alg import *
from tqdm import tqdm




set_of_values = [int(v) for v in np.arange(100, 261, 20)]


interval_time = timedelta(seconds=300)
data_generator = DataGenerator()  # TODO

number_of_requests = 50000
# number_of_drivers = 120  # 120 for synthetic
request_intervals = 30
avg_trip_distance = 15
lat_range = [30, 31]
long_range = [-98, -97]
unit_emission_range = [70, 300]
avg_speed = 40 / 3600  # 35 km/h
driver_move_range = [0.01, 0.01]
unassigned_tol = 10


fixedLimit_10 = FixedLimit_Alg(driver_move_range=driver_move_range, distance_limit=10)
fixedLimit_20 = FixedLimit_Alg(driver_move_range=driver_move_range, distance_limit=20)
fixedLimit_30 = FixedLimit_Alg(driver_move_range=driver_move_range, distance_limit=30)
distance_options = [1, 2, 5, 10, 15, 30]
gamma = 0.1
max_waiting_list = 20
V_coeff = 1
myAlg = MyAlg(driver_move_range=driver_move_range, distance_options=distance_options,
                          max_waiting_list=max_waiting_list, gamma=gamma, V_coeff=V_coeff, lr=0.1)


tora = TORA(threshold=1, base_ev_emission=70, driver_move_range=driver_move_range)

algorithms = {}
algorithms['TORA'] = tora
algorithms['MyAlg'] = myAlg
algorithms['Fixed-10'] = fixedLimit_10
algorithms['Fixed-20'] = fixedLimit_20
algorithms['Fixed-30'] = fixedLimit_30




for alg_name in algorithms:
    algorithm = algorithms[alg_name]
    algorithm.reset()
    algorithm_result = {}

    for number_of_drivers in set_of_values:
        data_generator.reset()
        data_generator.generate_synthetic_dataset(number_of_requests, number_of_drivers, request_intervals,
                                                  avg_trip_distance,
                                                  lat_range, long_range, unit_emission_range, avg_speed,
                                                  unassigned_tol=unassigned_tol, dist_of_unit_emission='exp',
                                                  random_gen_version=0)
        n_requests = len(data_generator.requests)

        print(f"\nAlg: {alg_name} - Dataset with {n_requests} requests and {len(data_generator.drivers)} drivers has been loaded.")
        with tqdm(total=len(data_generator.requests)) as pbar:
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

               # print(
               #     f"{batch_index}) Evaluating batch with {len(requests)} requests and {len(drivers)} drivers at {time}")
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
           'avg_emission': total_emission / data_generator.number_of_requests,
           'avg_waiting': total_waiting / data_generator.number_of_requests,
           'avg_deadhead': float(np.average(total_deadhead_distance)),
           'min_deadhead': float(np.min(total_deadhead_distance)),
           'max_deadhead': float(np.max(total_deadhead_distance)),
           'avg_tripdistance': float(np.average(total_trip_distance)),
           'n_requests': data_generator.number_of_requests,
           'n_unassignment': unassigned_requests,
           'serving_time': serving_time.seconds,
           'avg_req_intervals': data_generator.avg_intervals }

        algorithm_result[number_of_drivers] = total_info

    with open('results/Synthetic_drivers/{0}.json'.format(alg_name), 'w') as writer:
        json.dump(algorithm_result, writer)


