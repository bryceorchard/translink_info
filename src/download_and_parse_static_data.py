import os
import json
import csv
import requests
import zipfile
DIRECTORY = os.path.dirname(os.path.realpath(__file__))[:-4]

def download_static_data():
    url = "https://gtfs-static.translink.ca/gtfs/google_transit.zip"
    response = requests.get(url)

    with open(f"{DIRECTORY}/res/google_transit.zip", "wb") as f:
        f.write(response.content)
    with zipfile.ZipFile(f"{DIRECTORY}/res/google_transit.zip", 'r') as zip_ref:
        zip_ref.extract('stops.txt', f"{DIRECTORY}/res/")
        zip_ref.extract('trips.txt', f"{DIRECTORY}/res/")
    os.remove(f"{DIRECTORY}/res/google_transit.zip")

def parse_static_data():
    with open(f"{DIRECTORY}/res/stops.txt", "r", newline='') as csvfile:
        stops_reader = csv.reader(csvfile)
        stops = {}
        next(stops_reader)  # Skip header row
        for line in stops_reader:
            stops[line[1]] = line[0]
        with open(f"{DIRECTORY}/res/stops.json", "w") as file:
            file.write(json.dumps(stops))
    os.remove(f"{DIRECTORY}/res/stops.txt")

    with open(f"{DIRECTORY}/res/trips.txt", "r", newline='') as csvfile:
        trips_reader = csv.reader(csvfile)
        routes = {}
        next(trips_reader)  # Skip header row
        current_route_id = None
        for line in trips_reader:
            route_id = line[0]
            if route_id != current_route_id:
                if line[3] != "":
                    trip_number = line[3].split()[0]
                else:
                    trip_number = " "
                routes[trip_number] = route_id
                current_route_id = route_id

        with open(f"{DIRECTORY}/res/routes.json", "w") as file:
            file.write(json.dumps(routes))
    os.remove(f"{DIRECTORY}/res/trips.txt")

def main():
    """ Parses the static data if it hasn't already been parsed
    """
    if not os.path.exists(os.path.join(DIRECTORY, 'res', 'stops.json')) or not os.path.exists(os.path.join(DIRECTORY, 'res', 'routes.json')):
        download_static_data()
        parse_static_data()