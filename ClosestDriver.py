from Algorithm import *

class ClosestDriver(Algorithm):
    def __init__(self, driver_move_range):
        super().__init__(driver_move_range=driver_move_range)


    def algorithm_matcher(self, request, drivers, time, params=None):
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

