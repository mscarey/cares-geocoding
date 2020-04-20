import pytest

import geocoding


class TestGeocoding:
    def test_load_rows_from_csv(self):
        rows = geocoding.collect_rows()
        assert rows[0]["AssignedTo"] == "Matt"

    @pytest.mark.vcr()
    def test_get_coordinates_for_address(self, addresses):
        row = addresses[0]
        assert row["PropertyName"] == "Bell Stonebriar"
        latitude, longitude = geocoding.get_coordinates(row)
        assert 32 < latitude < 33
        assert -97 < longitude < -96
