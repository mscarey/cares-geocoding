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
        latitude, longitude = geocoding.get_coordinates(row)
        # 32.378061, -96.166077
        assert 32 < latitude < 33
        assert -97 < longitude < -96

    @pytest.mark.vcr()
    def test_get_likely_geocodes(self, addresses):
        row = addresses[2]
        assert row["PropertyName"] == "SPHINX AT MURDEAUX VILLAS"
        likely = [x for x in geocoding.get_likely_geocodes(row)]
        assert likely[0] == "Austin"

    def test_coordinates_changed(self, addresses):
        row = addresses[0]
        lat = 33.088442
        lng = -96.84384
        changed = geocoding.coordinates_changed(row, lat, lng)
        assert changed is True
