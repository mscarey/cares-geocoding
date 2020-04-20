import csv
from typing import Dict, List

MAPQUEST_KEY = "aun87npuivbHxsIUfgZyXMzPrRl9e7FA"


def collect_rows() -> List[Dict[str, str]]:
    with open("CARES_input.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        addresses = [row for row in reader]
    return addresses
