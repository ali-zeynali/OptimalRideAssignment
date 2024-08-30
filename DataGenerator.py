import numpy as np
import math
from Request import *
from Driver import *
import pandas as pd
import random

class DataGenerator:
    def __init__(self):
        self.reset()
    def reset(self):
        self.requests = None
        self.drivers = None
        self.head_index = 0
        self.number_of_requests = 0
        self.curr_time = None
        self.queue = []
        self.avg_intervals = 0

    def haversine_destination(self, lat1, lon1, distance, bearing):
        # Earth's radius in kilometers
        R = 6371.0

        # Convert latitude and longitude from degrees to radians
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)

        # Convert bearing to radians
        bearing = math.radians(bearing)

        # Calculate the new latitude
        lat2 = math.asin(math.sin(lat1) * math.cos(distance / R) +
                         math.cos(lat1) * math.sin(distance / R) * math.cos(bearing))

        # Calculate the new longitude
        lon2 = lon1 + math.atan2(math.sin(bearing) * math.sin(distance / R) * math.cos(lat1),
                                 math.cos(distance / R) - math.sin(lat1) * math.sin(lat2))

        # Convert latitude and longitude from radians to degrees
        lat2 = math.degrees(lat2)
        lon2 = math.degrees(lon2)

        return lat2, lon2

    def custom_exponential_sample(self, lam, low, high, version=1):
        # Generate a sample from the exponential distribution
        sample = np.random.exponential(scale=1 / lam)

        # Normalize the sample to a [0, 1] range (assuming the exponential distribution's range)
        # sample = 1 - np.exp(-sample * lam)  # Invert the distribution
        if version == 0:
            sample = 1 - np.exp(-sample * lam)
        else:
            sample = 1 - np.exp(-sample)

        # Scale and shift the sample to the [low, high] range
        scaled_sample = low + sample * (high - low)

        return scaled_sample

    def generate_synthetic_dataset(self, number_of_requests, number_of_drivers, request_intervals, avg_trip_distance,
                                  lat_range, long_range, unit_emission_range, avg_speed, unassigned_tol,
                                   dist_of_unit_emission='exp', random_gen_version=1):
        np.random.seed(42)
        time = datetime(2020, 1, 1, 0, 0, 0, 0)
        requests = []
        self.avg_intervals = request_intervals
        for i in range(number_of_requests):
            delta = np.random.normal(request_intervals, 3, 1)[0]
            if delta < 2:
                delta = 2
            delta = timedelta(seconds=delta)
            time += delta

            pickup_lat = np.random.uniform(lat_range[0], lat_range[1])
            pickup_long = np.random.uniform(long_range[0], long_range[1])
            trip_distance = np.random.normal(avg_trip_distance, 2, 1)[0]
            if trip_distance < 2:
                trip_distance = 2
            bearing = float(np.random.uniform(0, 360))
            dropoff_lat, dropoff_long = self.haversine_destination(pickup_lat, pickup_long, trip_distance, bearing)

            request = Request(i, time, pickup_lat, pickup_long, dropoff_lat, dropoff_long, unassigned_tol=unassigned_tol)
            requests.append(request)

        drivers = []
        for i in range(number_of_drivers):
            if dist_of_unit_emission == 'exp':
                unit_emission = self.custom_exponential_sample(2, unit_emission_range[0], unit_emission_range[1],
                                                               version=random_gen_version)
                # unit_emission = self.custom_exponential_sample(0.1, unit_emission_range[0], unit_emission_range[1])
            else:
                unit_emission = np.random.uniform(unit_emission_range[0], unit_emission_range[1])

            driver_lat = np.random.uniform(lat_range[0], lat_range[1])
            driver_long = np.random.uniform(long_range[0], long_range[1])
            driver = Driver(i, unit_emission, avg_speed=avg_speed, driver_lat=driver_lat, driver_long=driver_long)
            drivers.append(driver)

        self.requests = requests
        self.drivers = drivers
        self.number_of_requests = number_of_requests

    def read_dataset(self, path, number_of_drivers, avg_speed, unassigned_tol, lat_range, long_range, request_periods,
                     avg_trip_distance, unit_emission_range=None):
        data = pd.read_csv(path)
        data.sort_values(by='created_date', inplace=True)
        request_list = []
        intervals = []
        for index, row in data.iterrows():
            pickup_lat = float(row[15])
            pickup_long = float(row[14])
            dropoff_lat = float(row[5])
            dropoff_long = float(row[6])
            pickup_updated = False
            if pickup_lat < lat_range[0] or pickup_lat > lat_range[1]:
                pickup_lat = np.random.uniform(lat_range[0], lat_range[1])
                pickup_updated = True
            if pickup_long< long_range[0] or pickup_long > long_range[1]:
                pickup_long = np.random.uniform(long_range[0], long_range[1])
                pickup_updated = True

            # if dropoff_lat < lat_range[0] or dropoff_lat > lat_range[1]:
            #     dropoff_lat = np.random.uniform(lat_range[0], lat_range[1])
            # if dropoff_long < long_range[0] or dropoff_long > long_range[1]:
            #     dropoff_long = np.random.uniform(long_range[0], long_range[1])
            if pickup_updated:
                bearing = float(np.random.uniform(0, 360))
                trip_distance = np.random.normal(avg_trip_distance, 2, 1)[0]
                dropoff_lat, dropoff_long = self.haversine_destination(pickup_lat, pickup_long, trip_distance, bearing)

            request = Request(row[0], row[1],pickup_lat , pickup_long, dropoff_lat, dropoff_long, unassigned_tol=unassigned_tol)
            if request.created_request_time < request_periods[0] or request.created_request_time > request_periods[1]:
                continue

            if len(request_list) > 0:
                interval = request.created_request_time - request_list[-1].created_request_time
                interval = interval.seconds
                if interval < 5 * 60: # 5 minutes
                    intervals.append(interval)
            request_list.append(request)

        self.avg_intervals = np.average(intervals)



        driver_indexes = random.sample(range(len(data)), number_of_drivers)
        drivers_list = []
        for idx in driver_indexes:
            row = data.iloc[idx]
            if unit_emission_range is None:
                unit_emission = float(row[43])  # Default emission value
            else:
                # unit_emission = self.custom_exponential_sample(2, unit_emission_range[0], unit_emission_range[1])
                unit_emission = self.custom_exponential_sample(0.3, unit_emission_range[0], unit_emission_range[1])
            driver_lat = np.random.uniform(lat_range[0], lat_range[1])
            driver_long = np.random.uniform(long_range[0], long_range[1])
            driver = Driver(idx, unit_emission, avg_speed, driver_lat=driver_lat, driver_long=driver_long)
            drivers_list.append(driver)

        self.requests = request_list
        self.drivers = drivers_list
        self.number_of_requests = len(request_list)


    def next_batch(self, interval_time):
        if self.head_index >= self.number_of_requests:
            end_time = self.curr_time + interval_time
            self.curr_time += interval_time
            batch_requests = [request for request in self.queue]
            self.queue = []
            batch_drivers = [driver for driver in self.drivers if driver.time_to_free <= end_time]
            return batch_requests, batch_drivers, self.curr_time
        batch_requests = [request for request in self.queue]

        if self.curr_time is None:
            self.curr_time = self.requests[self.head_index].created_request_time

        if self.curr_time < self.requests[self.head_index].created_request_time:
            self.curr_time = self.requests[self.head_index].created_request_time

        end_time = self.curr_time + interval_time
        idx = self.head_index
        while idx < self.number_of_requests and self.requests[idx].created_request_time <= end_time:
            batch_requests.append(self.requests[idx])
            idx += 1
        self.head_index = idx
        self.queue = []

        batch_drivers = [driver for driver in self.drivers if driver.time_to_free <= end_time]
        self.curr_time += interval_time
        return batch_requests, batch_drivers, end_time

    def add_to_queue(self, request):
        request.unassigned_count += 1
        if request.unassigned_count <= request.unassigned_tol:
            self.queue.append(request)

    def get_all_requests(self):
        return self.requests

    def get_all_drivers(self):
        return self.drivers
