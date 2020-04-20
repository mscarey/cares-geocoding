import csv
from dataclasses import dataclass
import os
from typing import Dict, List, Tuple


from dotenv import load_dotenv
import requests

load_dotenv()

MAPQUEST_KEY = os.getenv("MAPQUEST_KEY")


def collect_rows() -> List[Dict[str, str]]:
    with open("CARES_input.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        addresses = [row for row in reader]
    return addresses


def make_full_address(row: Dict[str, str]):
    return f'{row["Address"]}, {row["City "]}, {row["State"]} {row["Zip"]}'


def request_geocode(row) -> Dict:
    full_address = make_full_address(row)
    response = requests.get(
        "http://www.mapquestapi.com/geocoding/v1/address",
        data={"key": MAPQUEST_KEY, "location": full_address, "maxResults": 1},
    ).json()
    return response


def get_coordinates(row) -> Tuple[float, float]:
    response = request_geocode(row)
    result = response["results"][0]
    lat = result["location"]["latLng"]["lat"]
    lng = result["location"]["latLng"]["lng"]
    return lat, lng
