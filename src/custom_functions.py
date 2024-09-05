import requests
import json
import os
DIRECTORY = os.path.dirname(os.path.realpath(__file__))[:-4]

with open(os.path.join(DIRECTORY, "res", "stops.txt"), 'r') as stops_txt:
    stops = [stop[:-1] for stop in stops_txt.readlines()]
with open(os.path.join(DIRECTORY, "res", "routes.txt"), 'r') as routes_txt:
    routes = [route[:-1] for route in routes_txt.readlines()]

def get_schedule(stop, route, key) -> list | str:
    """ Retrieves bus schedule information from the TransLink API
    """
    schedule = requests.get(f"http://api.translink.ca/rttiapi/v1/stops/{stop}/estimates?apikey={key}&routeNo={route}",
                            headers={'accept': 'application/JSON'})
    try:
        sjson = schedule.json()[0]
        # The API returns all of the JSON within a single list, so we must
        # access the first element to get the full JSON
    except:
        try:
            return schedule.json()['Code']
            # In the case of an error, we can access the error code
        except TypeError:
            # If no error code is generated from the api (json is blank)
            # Manually check inputs
            if stop not in stops:
                return '3002'
            if route not in routes:
                return '3004'
            return '3001'

    with open(os.path.join(DIRECTORY, 'res', 'schedule.json'), 'w') as file:
        json.dump(sjson, file, indent=4)
        # Write the API return to a JSON file in /res

    times = []

    # Loop through the next three bus times
    for i in range(0, 3):
        text = 'Next bus in' if i == 0 else 'In'
        data = sjson['Schedules'][i]
        # Access the corresponding upcoming buses

        expected_countdown = data['ExpectedCountdown']
        m_index = data['ExpectedLeaveTime'].index('m')
        # Index of the 'm' in pm/am
        expected_leave_time = data['ExpectedLeaveTime'][:m_index + 1]
        # Remove the pm/am from the time
        status = data['ScheduleStatus']
        times.append(
            f"{text} {expected_countdown} minute{'s' if expected_countdown != 1 else ''} "
            f"at {expected_leave_time}")
        match status:
            case '*':
                times.append(" - On time")
            case '-':
                times.append(" - Late")
            case '+':
                times.append(" - Early")
        
    return times