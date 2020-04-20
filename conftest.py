import json

import pytest

import geocoding


@pytest.fixture
def addresses():
    rows = geocoding.collect_rows()
    return rows


@pytest.fixture
def sphinx_location():
    location = """{"street":"12 North Murdeaux Lane",
    "adminArea6":"","adminArea6Type":"Neighborhood","adminArea5":"Dallas","adminArea5Type":"City",
    "adminArea4":"","adminArea4Type":"County","adminArea3":"TX","adminArea3Type":"State","adminArea1":"US",
    "adminArea1Type":"Country","postalCode":"75217","geocodeQualityCode":"L1CAA","geocodeQuality":"ADDRESS",
    "dragPoint":false,"sideOfStreet":"N","linkId":"US/ADDR/p1/34015471","unknownInput":"","type":"s",
    "latLng":{"lat":32.71327,"lng":-96.69299},"displayLatLng":{"lat":32.71327,"lng":-96.69299}}"""

    return json.loads(location)
