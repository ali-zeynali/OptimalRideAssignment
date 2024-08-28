from Algorithm import *


class MyAlg(Algorithm):
    def __init__(self, driver_move_range, distance_options, lr=0.1):
        super().__init__(driver_move_range=driver_move_range)
        self.distance_options = distance_options
        self.M = len(self.distance_options)
        self.utility_function = [np.log2(v / distance_options[0]) for v in distance_options]
        self.lr = lr

    def calculate_limit(self):
        return 50 #TODO

    def sort_with_indices(self, arr):
        sorted_indices = sorted(range(len(arr)), key=lambda x: arr[x])
        return sorted_indices

    def findDriver(self, request, drivers, time, params=None):
        if len(drivers) == 0:
            return None
        distance_limit = self.calculate_limit()
        distances = []
        emissions = []
        for driver in drivers:
            distance = self.calculate_distance(driver.curloc_lat, driver.curloc_long, request.pickup_lat,
                                               request.pickup_long)
            emission = (distance + request.trip_distance) * driver.unit_emission
            distances.append(distance)
            emissions.append(emission)

        if 'update' in params and params['update']:  # update utility functions
            sorted_distances = self.sort_with_indices(distances)
            emission_reduction_in_range = [0 for _ in range(self.M)]
            curr = 0
            closest_emission = emissions[sorted_distances[0]]
            for idx in sorted_distances:
                distance = distances[idx]
                emission_reduction = closest_emission - emissions[idx]
                if distance > self.distance_options[-1]:
                    break
                while distance > self.distance_options[curr]:
                    curr += 1
                emission_reduction_in_range[curr] = max(emission_reduction, emission_reduction_in_range[curr])
            for i in range(1, self.M):
                emission_reduction_in_range[i] = max(emission_reduction_in_range[i], emission_reduction_in_range[i - 1])

            for i in range(self.M):
                if emission_reduction_in_range[i] > 0:
                    self.utility_function[i] = self.utility_function[i] * (1- self.lr) + self.lr * emission_reduction_in_range[i]
            for i in range(1, self.M):
                self.utility_function[i] = max(self.utility_function[i], self.utility_function[i-1])



        emissions_in_range = [emissions[i] for i in range(len(emissions)) if distances[i] <= distance_limit]
        if len(emissions_in_range) == 0:
            return drivers[np.argmin(distances)]
        else:
            drivers_in_range = [drivers[i] for i in range(len(drivers)) if distances[i] <= distance_limit]
            return drivers_in_range[np.argmin(emissions_in_range)]
