from geopy.distance import great_circle
from datetime import datetime, timedelta
import numpy as np

class Algorithm:
    def __init__(self, driver_move_range=[0, 0]):
        self.driver_move_range = driver_move_range

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        point1 = (lat1, lon1)
        point2 = (lat2, lon2)
        distance = great_circle(point1, point2).km
        return distance

    def reset(self):
        return

    def findDriver(self, request, drivers, time, closest_at_end=False, params=None):
        if request.unassigned_count < request.unassigned_tol or not closest_at_end:
            return self.algorithm_matcher(request, drivers, time, params=params)
        else:
            return self.get_closest(request, drivers)


    def algorithm_matcher(self, request, drivers, time, params=None):
        return None

    def get_closest(self, request, drivers):
        if len(drivers) == 0:
            return None
        closest_driver = None
        closest_distance = float('inf')
        for driver in drivers:
            distance = self.calculate_distance(driver.curloc_lat, driver.curloc_long, request.pickup_lat, request.pickup_long)
            if distance < closest_distance:
                closest_distance = distance
                closest_driver = driver
        return closest_driver

    def finalize_match(self, request, driver, time, params=None):
        request.matched_driver = driver.driver_id
        driver.matched_requests.append(request.ride_request_id)
        deadhead_distance = self.calculate_distance(driver.curloc_lat, driver.curloc_long, request.pickup_lat, request.pickup_long)
        waiting_time = (time - request.created_request_time) + timedelta(seconds=deadhead_distance/driver.avg_speed)
        waiting_time = waiting_time.total_seconds()

        driver.trip_distances.append(request.trip_distance)
        driver.deadhead_distances.append(deadhead_distance)
        driver.driver_utility += request.trip_distance  - deadhead_distance

        request.deadhead_distance = deadhead_distance
        request.waiting_time = waiting_time
        request.time_in_batch = (time - request.created_request_time).total_seconds()
        request.emission = (deadhead_distance + request.trip_distance) * driver.unit_emission

        move_lat = np.random.uniform(-self.driver_move_range[0], self.driver_move_range[0])
        move_long = np.random.uniform(-self.driver_move_range[1], self.driver_move_range[1])
        driver.curloc_lat = request.dropoff_lat + move_lat
        driver.curloc_long = request.dropoff_long + move_long
        driver.time_to_free = time + timedelta(seconds=(deadhead_distance + request.trip_distance)/ driver.avg_speed)
