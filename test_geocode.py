import pytest

import geocoding


class TestGeocoding:
    def test_load_rows_from_csv(self):
        rows = geocoding.collect_rows()
        assert rows[0]["AssignedTo"] == "Matt"

    def test_make_address_from_row(self, addresses):
        row = addresses[0]
        full_address = "5250 Town and Country Boulevard, Frisco, TX 75034"
        assert geocoding.make_full_address(row) == full_address

    @pytest.mark.vcr()
    def test_get_coordinates_for_address(self, addresses):
        row = addresses[0]
        assert row["PropertyName"] == "Bell Stonebriar"
        latitude, longitude = geocoding.get_coordinates(row)
        # 32.378061, -96.166077
        assert 32 < latitude < 33
        assert -97 < longitude < -96
