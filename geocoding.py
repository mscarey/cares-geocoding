"""
Use Mapquest API to find likely addresses and coordinates for apartment buildings.

Only generates an update if a coordinate returned by the API differs from the existing
coordinates by at least 0.005.
"""

import csv
import os
from typing import Dict, Iterator, List, Optional, Tuple


from dotenv import load_dotenv
import requests

load_dotenv()

MAPQUEST_KEY = os.getenv("MAPQUEST_KEY")

SIGNIFICANT_DISTANCE = 0.005


def collect_rows() -> List[Dict[str, str]]:
    with open("CARES_input.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        addresses = [row for row in reader]
    return addresses


def make_full_address(row: Dict[str, str]):
    return f'{row["PropertyName"]}, {row["Address"]}, {row["City "]}, {row["State"]}'


def request_geocode(row: Dict[str, str]) -> Dict:
    full_address = make_full_address(row)
    response = requests.get(
        "http://www.mapquestapi.com/geocoding/v1/address",
        params={"key": MAPQUEST_KEY, "location": full_address, "maxResults": 5},
    ).json()
    return response


def get_likely_location(row) -> Optional[Dict]:
    """Accept only a geocode that gets the zip code right."""
    response = request_geocode(row)
    for location in response["results"][0]["locations"]:
        if location["postalCode"][:5] == row["Zip"][:5] and location[
            "geocodeQuality"
        ] in ("ADDRESS", "POINT"):
            return location
    return None


def response_coordinates_differ_from_csv(csv_row: Dict, api_location: Dict) -> bool:
    if (
        abs(float(csv_row["Latitude"]) - api_location["latLng"]["lat"])
        > SIGNIFICANT_DISTANCE
    ):
        return True
    if (
        abs(float(csv_row["Longitude"]) - api_location["latLng"]["lng"])
        > SIGNIFICANT_DISTANCE
    ):
        return True
    return False


def make_geocode_update(csv_row: Dict, api_location: Dict) -> Dict:
    """Make an update for one location, assuming an update is needed."""
    update = {"PropertyID": csv_row["PropertyID"]}
    update["Address"] = api_location.get("street")
    update["Latitude"] = api_location["latLng"]["lat"]
    update["Longitude"] = api_location["latLng"]["lng"]
    if api_location.get("intersection"):
        update["Intersection"] = api_location.get("intersection")

    for colnum in range(1, 7):
        colname = api_location.get(f"adminArea{colnum}Type")
        colval = api_location.get(f"adminArea{colnum}")

        if colname and colval:
            update[colname] = colval
    return update


def get_update_for_row_if_needed(csv_row: Dict) -> Optional[Dict]:
    location = get_likely_location(csv_row)
    if location and response_coordinates_differ_from_csv(csv_row, location):
        return make_geocode_update(csv_row, location)
    return None


def make_address_updates() -> Iterator[Dict]:
    csv_rows = collect_rows()
    for csv_row in csv_rows:
        if csv_row["Status"] == "Incomplete":
            update = get_update_for_row_if_needed(csv_row)
            if update is not None:
                yield update


def save_updates_as_csv():
    with open("updates.csv", "w") as csvfile:
        fieldnames = [
            "PropertyID",
            "Address",
            "Latitude",
            "Longitude",
            "Country",
            "State",
            "County",
            "City",
            "Neighborhood",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row_dict in make_address_updates():
            writer.writerow(row_dict)


if __name__ == "__main__":
    save_updates_as_csv()
