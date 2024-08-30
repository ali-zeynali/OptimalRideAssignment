from datetime import datetime, timedelta
import pytz
from geopy.distance import great_circle


class Request:
    def __init__(self, ride_request_id, created_request_time, pickup_lat, pickup_long, dropoff_lat, dropoff_long, unassigned_tol=3):
        self.ride_request_id = int(ride_request_id)
        self.created_request_time = self.string_to_time(created_request_time) if isinstance(created_request_time, str) else created_request_time
        self.pickup_lat = float(pickup_lat)
        self.pickup_long = float(pickup_long)
        self.dropoff_lat = float(dropoff_lat)
        self.dropoff_long = float(dropoff_long)
        self.trip_distance = self.calculate_distance(self.pickup_lat, self.pickup_long, self.dropoff_lat,
                                                     self.dropoff_long)
        self.deadhead_distance = -1
        self.emission = -1
        self.time_in_batch = 0
        self.waiting_time = 0
        self.matched_driver = None
        self.unassigned_tol = unassigned_tol
        self.unassigned_count = 0

    def string_to_time(self, timestamp):
        time1 = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S%z")
        time1_UTC = time1.astimezone(pytz.utc).replace(tzinfo=None)
        return time1_UTC

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        point1 = (lat1, lon1)
        point2 = (lat2, lon2)
        distance = great_circle(point1, point2).km
        return distance
