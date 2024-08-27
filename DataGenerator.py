import numpy as np
import math
from Request import *
from Driver import *


class DataGenerator:
    def __init__(self):
        self.requests = None
        self.drivers = None
        self.head_index = 0
        self.number_of_requests = 0
        self.curr_time = None

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

    def custom_exponential_sample(self, lam, low, high):
        # Generate a sample from the exponential distribution
        sample = np.random.exponential(scale=1 / lam)

        # Normalize the sample to a [0, 1] range (assuming the exponential distribution's range)
        sample = 1 - np.exp(-sample * lam)  # Invert the distribution

        # Scale and shift the sample to the [low, high] range
        scaled_sample = low + sample * (high - low)

        return scaled_sample

    def generate_synthetic_dataset(self, number_of_requests, number_of_drivers, request_intervals, avg_trip_distance,
                                  lat_range, long_range, unit_emission_range,avg_speed, dist_of_unit_emission='exp'):
        # np.random.seed(42)
        time = datetime(2020, 1, 1, 0, 0, 0, 0)
        requests = []
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

            request = Request(i, time, pickup_lat, pickup_long, dropoff_lat, dropoff_long)
            requests.append(request)

        drivers = []
        for i in range(number_of_drivers):
            if dist_of_unit_emission == 'exp':
                unit_emission = self.custom_exponential_sample(1, unit_emission_range[0], unit_emission_range[1])
            else:
                unit_emission = np.random.uniform(unit_emission_range[0], unit_emission_range[1])

            driver_lat = np.random.uniform(lat_range[0], lat_range[1])
            driver_long = np.random.uniform(long_range[0], long_range[1])
            driver = Driver(i, unit_emission, avg_speed=avg_speed, driver_lat=driver_lat, driver_long=driver_long)
            drivers.append(driver)

        self.requests = requests
        self.drivers = drivers
        self.number_of_requests = number_of_requests

    def next_batch(self, interval_time):
        if self.head_index >= self.number_of_requests:
            return [], [], self.curr_time
        batch_requests = []

        if self.curr_time is None:
            self.curr_time = self.requests[self.head_index].created_request_time

        if self.curr_time < self.requests[self.head_index].created_request_time:
            self.curr_time = self.requests[self.head_index].created_request_time

        end_time = self.curr_time + interval_time
        idx = self.head_index
        while idx < self.number_of_requests and self.requests[idx].created_request_time <= end_time:
            batch_requests.append(self.requests[idx])
            idx += 1

        batch_drivers = [driver for driver in self.drivers if driver.time_to_free <= end_time]
        self.curr_time += interval_time
        return batch_requests, batch_drivers, end_time

    def next(self):
        self.head_index += 1

    def get_all_requests(self):
        return self.requests

    def get_all_drivers(self):
        return self.drivers
