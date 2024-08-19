from datetime import datetime



class Driver:

    def __init__(self, driver_id, unit_emission, avg_speed, driver_lat=None, driver_long=None):
        self.driver_id = driver_id
        self.unit_emission = unit_emission
        self.init_lat = driver_lat
        self.init_long = driver_long
        self.avg_speed = avg_speed

        self.reset()

    def reset(self, ):
        self.driver_utility = 0
        self.trip_distances = []
        self.deadhead_distances = []
        self.matched_requests = []

        self.curloc_lat = self.init_lat
        self.curloc_long = self.init_long

        self.time_to_free = datetime(2010, 1, 1, 0, 0, 0)
