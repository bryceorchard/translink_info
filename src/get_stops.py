import os
import re
DIRECTORY = os.path.dirname(os.path.realpath(__file__))[:-4]

with open(f"{DIRECTORY}/res/google_transit/stops.txt", "r") as file:
    stops = file.readlines()
    with open(f"{DIRECTORY}/res/stops.txt", "w") as file2:
        
        for line in stops[1:]:
            pattern = r",\d{5},"
            match = re.findall(pattern, line)[0][1:-1]
            file2.write(f"{match}\n")