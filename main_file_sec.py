import os
from DataGenerator import *
from FixedLimit_Alg import *
import json
from datetime import datetime, timedelta
import numpy as np

interval_time = timedelta(seconds=300)
distance_limits = range(10, 46, 5)
number_of_requests = 5000
number_of_drivers = 250
request_intervals = 30
avg_trip_distance = 15
lat_range = [30, 31]
long_range = [-98, -97]
unit_emission_range = [70, 300]
avg_speed = 40 / 3600  # km/h
driver_move_range = [0.01, 0.01]

all_results = {
    'total_info': {}
}

num_trials = 10

for distance_limit in distance_limits:
    print(f"Running simulation for distance_limit = {distance_limit} km")

    accum_emission = 0
    accum_waiting = 0
    accum_deadhead_distance = []
    accum_trip_distance = []

    for trial in range(num_trials):
        print(f"Trial {trial + 1}/{num_trials} for distance_limit = {distance_limit} km")

        data_generator = DataGenerator()
        data_generator.generate_synthetic_dataset(number_of_requests, number_of_drivers, request_intervals,
                                                  avg_trip_distance,
                                                  lat_range, long_range, unit_emission_range, avg_speed,
                                                  dist_of_unit_emission='exp')

        algorithm = FixedLimit_Alg(driver_move_range=driver_move_range, distance_limit=distance_limit)

        batch_index = 0
        while True:
            requests, drivers, time = data_generator.next_batch(interval_time=interval_time)
            if len(requests) == 0:
                break
            if len(drivers) == 0:
                continue

            print(f"  Batch {batch_index} with {len(requests)} requests and {len(drivers)} drivers at {time}")
            batch_index += 1

            for request in requests:
                driver = algorithm.findDriver(request, drivers, time)
                if driver is not None:
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

        for request in requests:
            total_emission += float(request.emission)
            total_waiting += request.waiting_time
            total_deadhead_distance.append(request.deadhead_distance)
            total_trip_distance.append(request.trip_distance)

        accum_emission += total_emission
        accum_waiting += total_waiting
        accum_deadhead_distance.extend(total_deadhead_distance)
        accum_trip_distance.extend(total_trip_distance)

    avg_emission = accum_emission / (number_of_requests * num_trials)
    avg_waiting = accum_waiting / (number_of_requests * num_trials)
    avg_deadhead = float(np.average(accum_deadhead_distance))
    min_deadhead = float(np.min(accum_deadhead_distance))
    max_deadhead = float(np.max(accum_deadhead_distance))
    avg_tripdistance = float(np.average(accum_trip_distance))

    all_results['total_info'][f'distance_limit_{distance_limit}'] = {
        'avg_emission': avg_emission,
        'avg_waiting': avg_waiting,
        'avg_deadhead': avg_deadhead,
        'min_deadhead': min_deadhead,
        'max_deadhead': max_deadhead,
        'avg_tripdistance': avg_tripdistance,
        'n_requests': number_of_requests,
        'n_trials': num_trials
    }

    print(f"Completed all {num_trials} trials for distance_limit = {distance_limit} km\n")

results_dir = '.'
os.makedirs(results_dir, exist_ok=True)

with open(f'results/all_distance_limits_results.json', 'w') as writer:
    json.dump(all_results, writer)

print("All simulations completed. Results saved to 'all_distance_limits_results.json'")
