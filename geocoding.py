import csv
import os
from typing import Dict, Iterator, List, Optional, Tuple


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
    return f'{row["PropertyName"]}, {row["Address"]}, {row["City "]}, {row["State"]}'


def request_geocode(row) -> Dict:
    full_address = make_full_address(row)
    response = requests.get(
        "http://www.mapquestapi.com/geocoding/v1/address",
        params={"key": MAPQUEST_KEY, "location": full_address, "maxResults": 5},
    ).json()
    return response


def get_likely_geocodes(row) -> Optional[Dict]:
    """Accept only the geocodes that get the zip code right."""
    response = request_geocode(row)
    for location in response["results"][0]["locations"]:
        if location["postalCode"][:5] == row["Zip"][:5]:
            return location
    return None


def coordinates_changed(row: Dict, lat: float, lng: float) -> bool:
    if abs(float(row["Latitude"]) - lat) > 0.01:
        return True
    if abs(float(row["Longitude"]) - lng) > 0.01:
        return True
    return False


def get_coordinates(location: Dict) -> Tuple[float, float]:
    lat = location["latLng"]["lat"]
    lng = location["latLng"]["lng"]
    return lat, lng
