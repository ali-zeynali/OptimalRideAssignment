from Algorithm import *
import numpy as np

class FixedLimit_Alg(Algorithm):
    def __init__(self, distance_limit, driver_move_range, lr=0.1):
        super().__init__(driver_move_range=driver_move_range)
        self.distance_limit = distance_limit # set it to zero to have closest driver assignment
        self.closest_emission = 0
        self.emission_reduction = 0
        self.lr = lr

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
        closest_emission = emissions[np.argmin(distances)]
        self.closest_emission = self.closest_emission * (1-self.lr) + self.lr * closest_emission

        emissions_in_range = [emissions[i] for i in range(len(emissions)) if distances[i] <= self.distance_limit]
        if len(emissions_in_range) == 0:
            return drivers[np.argmin(distances)]
            # return None
        else:
            drivers_in_range = [drivers[i] for i in range(len(drivers)) if distances[i] <= self.distance_limit]
            emission_reduction = closest_emission - min(emissions_in_range)
            self.emission_reduction = (1-self.lr) * self.emission_reduction + self.lr * emission_reduction
            return drivers_in_range[np.argmin(emissions_in_range)]
