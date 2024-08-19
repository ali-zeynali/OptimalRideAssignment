from Algorithm import *
import numpy as np

class FixedLimit_Alg(Algorithm):
    def __init__(self, distance_limit, driver_move_range):
        super().__init__(driver_move_range=driver_move_range)
        self.distance_limit = distance_limit # set it to zero to have closest driver assignment

    def findDriver(self, request, drivers, time, params=None):
        if len(drivers) == 0:
            return None
        distances = []
        emissions = []
        for driver in drivers:
            distance = self.calculate_distance(driver.curloc_lat, driver.curloc_long, request.pickup_lat, request.pickup_long)
            emission = (distance + request.trip_distance) * driver.unit_emission
            distances.append(distance)
            emissions.append(emission)

        emissions_in_range = [emissions[i] for i in range(len(emissions)) if distances[i] <= self.distance_limit]
        if len(emissions_in_range) == 0:
            return drivers[np.argmin(distances)]
        else:
            drivers_in_range = [drivers[i] for i in range(len(drivers)) if distances[i] <= self.distance_limit]
            return drivers_in_range[np.argmin(emissions_in_range)]
