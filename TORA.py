from Algorithm import *


class TORA(Algorithm):

    def __init__(self, threshold, base_ev_emission, driver_move_range=[0, 0]):
        super().__init__(driver_move_range=driver_move_range)
        self.base_ev_emission = base_ev_emission
        self.threshold = threshold

    def findDriver(self, request, drivers, time, params=None):
        distances = []
        unit_emissions = []
        driver_index = []
        waiting_times = []

        for i, driver in enumerate(drivers):
            # if driver.availability:
            distance = self.calculateDistance(request.pickup_lat, request.pickup_long, driver.curloc_lat,
                                              driver.curloc_long)
            distances.append(distance)
            waiting_times.append(self.get_waiting_time(driver, time, distance))
            driver_index.append(i)
            if driver.unit_emission is not None:
                unit_emissions.append(driver.unit_emission)

        if len(distances) == 0:
            return None
        distances = np.array(distances)
        unit_emissions = np.array(unit_emissions)
        emissions = distances * unit_emissions
        waiting_times = np.array(waiting_times)

        bestCarIndex = np.argmin(waiting_times)
        bestDriverIndex = driver_index[bestCarIndex]

        if waiting_times[bestCarIndex] == 0:
            return drivers[bestDriverIndex]

        distance_diff = (waiting_times - waiting_times[bestCarIndex]) * drivers[bestCarIndex].avg_speed

        for i in range(len(distance_diff)):
            if distance_diff[i] == 0:
                distance_diff[i] = 1e-6

        emission_to_distance = (emissions[bestCarIndex] - emissions) / distance_diff
        best_alternate_Index = np.argmax(emission_to_distance)
        best_alternate_Driver_index = driver_index[best_alternate_Index]

        if emission_to_distance[best_alternate_Index] > self.threshold * self.base_ev_emission:
            return drivers[best_alternate_Driver_index]
        else:
            return drivers[bestDriverIndex]

    def get_waiting_time(self, driver, time, dist_driver_to_passenger):

        if time >= driver.time_to_free:
            waiting_time = 0
        else:
            waiting_time = (driver.time_to_free - time).seconds

        waiting_time += dist_driver_to_passenger / driver.avg_speed
        return waiting_time

    def calculateDistance(self, lat1, lon1, lat2, lon2):
        point1 = (lat1, lon1)
        point2 = (lat2, lon2)
        distance = great_circle(point1, point2).km
        return distance
