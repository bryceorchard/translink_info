import requests
from google.transit import gtfs_realtime_pb2
import json
import time
import os

def get_schedule(stop, route, key) -> list | str:
    """ Retrieves bus schedule information from the TransLink API
    """

    DIRECTORY = os.path.dirname(os.path.realpath(__file__))[:-4]

    with open(os.path.join(DIRECTORY, "res", "stops.json"), 'r') as file:
        stops = json.load(file)
    with open(os.path.join(DIRECTORY, "res", "routes.json"), 'r') as file:
        routes = json.load(file)


    url = "https://gtfsapi.translink.ca/v3/gtfsrealtime"
    response = requests.get(url, params={"apikey": key}, timeout=10)
    response.raise_for_status()

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    with open(os.path.join(DIRECTORY, 'res', 'api_response.json'), 'w') as file:
        file.write(str(feed))

    stop_exists = False
    for key, value in stops.items():
        if key == stop:
            stop_id = value
            stop_exists = True

    route_exists = False
    for key, value in routes.items():
        if key == route:
            route_id = value
            route_exists = True

    if not stop_exists and not route_exists:
        return 'stop and route do not exist'
    if not stop_exists:
        return 'stop does not exist'
    if not route_exists:
        return 'route does not exist'

    stop_id = stops[stop]
    route_id = routes[route]
    
    route_exists = False

    count = 0
    times = []

    for entity in feed.entity:
        if not entity.HasField("trip_update"):
            continue
        trip_update = entity.trip_update
        trip = trip_update.trip
        if trip.route_id != route_id:
            continue
        for stop_time_update in trip_update.stop_time_update:
            if stop_time_update.stop_id != stop_id:
                continue

            route_exists = True
            text = 'Next bus in' if count == 0 else 'In'
            expected_arrival_time = int((int(stop_time_update.arrival.time) - time.time())//60)
            delay = int(int(stop_time_update.arrival.delay)//60)

            times.append(f"{text} {expected_arrival_time} minute{'s' if expected_arrival_time != 1 else ''}")
            if delay == 0:
                times.append(" - On time")
            if delay < 0:
                times.append(f" - Early by {delay*-1} minute{'s' if delay != -1 else ''}")
            if delay > 0:
                times.append(f" - Late by {delay} minute{'s' if delay != 1 else ''}")
            count+=1
        if count == 3:
            break
    if not route_exists:
        return 'route does not exist'
    return times