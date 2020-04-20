import pytest

import geocoding


class TestGeocoding:
    def test_load_rows_from_csv(self):
        rows = geocoding.collect_rows()
        assert rows[0]["AssignedTo"] == "Matt"

    def test_make_address_from_row(self, addresses):
        row = addresses[0]
        full_address = "5250 Town and Country Boulevard, Frisco, TX"
        assert full_address in geocoding.make_full_address(row)

    @pytest.mark.vcr()
    def test_get_coordinates_for_address(self, addresses):
        row = addresses[0]
        assert row["PropertyName"] == "Bell Stonebriar"
        response = geocoding.request_geocode(row)
        assert response["results"][0]["locations"][0]["street"].startswith("5250 Town")

    @pytest.mark.vcr()
    def test_get_likely_geocodes(self, addresses):
        row = addresses[2]
        assert row["PropertyName"] == "SPHINX AT MURDEAUX VILLAS"
        likely = geocoding.get_likely_geocode(row)
        assert likely["street"] == "12 North Murdeaux Lane"

    def test_response_coordinates_differ_from_csv(self, addresses, sphinx_location):
        row = addresses[0]
        changed = geocoding.response_coordinates_differ_from_csv(row, sphinx_location)
        assert changed is True

    def test_make_geocode_update(self, addresses, sphinx_location):
        row = addresses[2]
        update = geocoding.make_geocode_update(
            csv_row=row, api_location=sphinx_location
        )
        assert update["PropertyID"] == "11335188"
        assert update["Address"] == "12 North Murdeaux Lane"
        assert update["Latitude"] == 32.71327
